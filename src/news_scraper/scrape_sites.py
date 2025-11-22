# src/news_scraper/scrape_sites.py

"""
Contains the main scraping class for Middle East geopolitics news,
using Ollama for structured data extraction.
"""

import uuid
import hashlib
import json
from typing import List, Dict, Any, Optional

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pydantic import BaseModel, Field, ValidationError

import ollama

# Import the IngestData class from the local package
from .ingest_data import IngestData


# --- 1. Pydantic Schema for LLM Output ---
# This defines the exact JSON structure we want the LLM to return.
class ArticleData(BaseModel):
    """Defines the structure for a single scraped news article."""

    url: str = Field(..., description="The definitive URL of the article.")
    publication_date: str = Field(
        ..., description="The date the article was published in YYYY-MM-DD format."
    )
    headline: str = Field(..., description="The main title or headline of the article.")
    article_body: str = Field(
        ...,
        description="The complete text content of the article, cleaned of advertisements and boilerplate.",
    )
    source_name: str = Field(
        ..., description="The name of the news organization that published the article."
    )


class ExtractedArticles(BaseModel):
    """Container for a list of articles extracted from a single page."""

    articles: List[ArticleData] = Field(
        ..., description="List of all unique news articles found on the page."
    )


# Define the expected DataFrame columns (matching ingestion schema)
SCRAPE_COLUMNS = [
    "article_id",
    "url",
    "publication_date",
    "headline",
    "article_body",
    "source_name",
    "scraper_run_id",
    "scraped_at",
]


class NewsScraper:
    """
    Manages the end-to-end scrape-extract-load workflow.
    """

    # Use a small, efficient model for structured extraction
    OLLAMA_MODEL = "llama3"

    def __init__(self, site_name: str, base_url: str):
        self.site_name = site_name
        self.base_url = base_url
        self.run_id = str(uuid.uuid4())
        self.ingestor = IngestData()
        self.logger = self.ingestor.logger
        self.logger.info(
            "NewsScraper initialized for site: %s. Run ID: %s",
            self.site_name,
            self.run_id,
        )

    def fetch_page(self, url: str) -> Optional[str]:
        """Fetches the content of a single URL."""
        self.logger.info("Attempting to fetch URL: %s", url)
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            self.logger.info("Successfully fetched URL: %s", url)
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error("Failed to fetch %s: %s", url, e)
            return None

    def _clean_html_for_llm(self, html_content: str) -> str:
        """Strips out boilerplate elements (scripts, styles) to focus LLM on content."""
        soup = BeautifulSoup(html_content, "html.parser")
        for script_or_style in soup(
            ["script", "style", "header", "footer", "nav", "aside"]
        ):
            script_or_style.decompose()
        return soup.get_text(separator=" ", strip=True)

    def extract_with_ollama(self, html_content: str) -> List[Dict[str, Any]]:
        """
        Uses Ollama to extract structured data from raw HTML content.
        """
        cleaned_text = self._clean_html_for_llm(html_content)
        self.logger.info(
            "Sending %d characters of cleaned text to Ollama...", len(cleaned_text)
        )

        prompt = (
            f"You are an expert geopolitical news data extractor. Analyze the following document from {self.site_name}. "
            "Extract ALL unique news articles related to Middle East geopolitics. "
            "The output MUST be a valid JSON object that strictly conforms to the provided JSON schema."
            f"\n\n--- DOCUMENT START ---\n\n{cleaned_text[:10000]}"  # Limit size to prevent token overflow
        )

        try:
            response = ollama.generate(
                model=self.OLLAMA_MODEL,
                prompt=prompt,
                format="json",
                options={"temperature": 0.1},  # Low temperature for reliable structure
                # Provide the JSON schema generated from the Pydantic model
                # The LLM uses this to ensure output compliance
                # response_format=ExtractedArticles.model_json_schema() # Note: Ollama client may require a direct schema string depending on version
            )

            # Ollama response structure can vary; we expect the structured JSON in response['response'] or similar field
            raw_json_string = (
                response["response"]
                if "response" in response
                else response.get("message", {}).get("content", "{}")
            )

            # 1. Parse JSON
            raw_data = json.loads(raw_json_string)

            # 2. Validate and Structure with Pydantic
            validated_data = ExtractedArticles.model_validate(raw_data)

            # Convert Pydantic models back to simple list of dictionaries
            extracted_list = [
                article.model_dump() for article in validated_data.articles
            ]
            self.logger.info(
                "Ollama successfully extracted and validated %d articles.",
                len(extracted_list),
            )
            return extracted_list

        except (KeyError, json.JSONDecodeError, ValidationError) as e:
            self.logger.error("Ollama extraction failed (JSON/Pydantic Error): %s", e)
            self.logger.debug("Raw Ollama output: %s", response)
            return []
        except Exception as e:
            self.logger.error("Ollama execution error: %s", e)
            return []

    def execute_run(self, urls_to_scrape: List[str]) -> pd.DataFrame:
        """
        Executes the full scrape-extract-load workflow for a list of URLs.
        """
        self.logger.info(
            "--- Starting Scraping Run %s for %d URLs ---",
            self.run_id,
            len(urls_to_scrape),
        )

        all_scraped_data = []

        for url in urls_to_scrape:
            html_content = self.fetch_page(url)
            if html_content:
                raw_articles = self.extract_with_ollama(html_content)

                # Enrich data with required metadata (run_id, article_id, timestamp)
                for article in raw_articles:
                    # Create a unique article_id using a hash of the URL
                    article["article_id"] = hashlib.sha256(
                        article["url"].encode("utf-8")
                    ).hexdigest()
                    article["scraper_run_id"] = self.run_id
                    article["scraped_at"] = pd.Timestamp.now(tz="UTC")
                    all_scraped_data.append(article)

        # 3. Transform (Create DataFrame)
        df = pd.DataFrame(all_scraped_data, columns=SCRAPE_COLUMNS)
        self.logger.info("Total unique articles ready for ingestion: %d", len(df))

        # 4. Load (Ingestion)
        # The IngestData class already handles table existence check
        rows_loaded = self.ingestor.load_data(df, if_exists="append")

        self.logger.info(
            "--- Scraping Run %s Completed. %d rows loaded. ---",
            self.run_id,
            rows_loaded,
        )
        return df
