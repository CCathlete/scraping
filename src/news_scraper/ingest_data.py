# src/news_scraper/ingest_data.py

"""
Handles database setup and data ingestion (Load part of ETL) for the
geopolitics news scraper. Uses the published 'doggopyr' helper package.
"""

from typing import Optional, Literal
import pandas as pd

from doggopyr.tools.helper_functions import Module as hf

db_engine, project_root, input_files, log_dir, logger = hf.init_locations_and_dotenv(
    project_root_marker="src"
)


class IngestData:
    """
    Initializes environment and provides methods for interacting with the database.

    This class handles:
    1. Initializing the engine and logging via doggopyr.
    2. Ensuring the target table exists.
    3. Loading a DataFrame into the target table.
    """

    # Define the target PostgreSQL table name
    TARGET_TABLE = "geopolitics_news"

    # Define the DDL statement for the news table
    CREATE_SQL_DDL = f"""
    CREATE TABLE IF NOT EXISTS {TARGET_TABLE} (
        article_id VARCHAR(255) PRIMARY KEY,
        url TEXT NOT NULL UNIQUE,
        publication_date DATE,
        headline TEXT NOT NULL,
        article_body TEXT,
        source_name VARCHAR(255),
        scraper_run_id VARCHAR(50),
        scraped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """

    def __init__(self):
        """
        Initializes the database engine and logging using the helper package.
        """
        # hf.init_locations_and_dotenv loads .env, sets up logging, and creates the engine
        self.engine, self.project_root, _, self.log_dir, self.logger = (
            hf.init_locations_and_dotenv(
                logger_name="NewsIngestor",
                log_file_prefix="geopolitics_ingest",
                project_root_marker="src",  # Assumes 'src' is the marker in the new repo
            )
        )
        self.logger.info("News Ingestor initialized and engine created.")
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        """Ensures the target table exists before any scraping occurs."""
        self.logger.info("Ensuring target table '%s' exists...", self.TARGET_TABLE)
        try:
            # Uses the helper function to execute DDL
            hf.execute_query(self.CREATE_SQL_DDL, engine=self.engine)
            self.logger.info("Table '%s' is ready.", self.TARGET_TABLE)
        except Exception as e:
            self.logger.error("Failed to create table %s: %s", self.TARGET_TABLE, e)
            raise

    def load_data(
        self,
        df: pd.DataFrame,
        if_exists: Literal["append", "replace", "fail"] = "append",
        chunksize: Optional[int] = 1000,
    ) -> int | None:
        """Loads a DataFrame of scraped news into the PostgreSQL table."""
        if df.empty:
            self.logger.warning("DataFrame is empty. Skipping load.")
            return 0

        self.logger.info(
            "Starting load of %d articles into table '%s'.", len(df), self.TARGET_TABLE
        )
        try:
            # Use pandas to_sql for efficient bulk insertion
            rows_inserted = df.to_sql(
                name=self.TARGET_TABLE,
                con=self.engine,
                if_exists=if_exists,
                index=False,
                chunksize=chunksize,
            )
            self.logger.info(
                "Successfully loaded %d rows into table '%s'.",
                rows_inserted,
                self.TARGET_TABLE,
            )
            return rows_inserted

        except Exception as e:
            # This is common for UNIQUE or PRIMARY KEY violations when scraping
            # the same articles again.
            self.logger.error(
                "Error loading data into table %s (often due to duplicates): %s",
                self.TARGET_TABLE,
                e,
            )
            # Return 0 inserted rows on failure to reflect the state
            return 0
