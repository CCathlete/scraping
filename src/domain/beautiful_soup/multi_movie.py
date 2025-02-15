"""Scraping data of a multiple movies from subslikescript.com """

# Imports.
from typing import Union
from bs4 import BeautifulSoup
from bs4.element import (
    Tag,
    PageElement,
    ResultSet,
)
import requests
from typing_extensions import TypeAlias
from src.domain.beautiful_soup.one_movie import get_movie_info

# Helpers.
UpToOneElement: TypeAlias = Union[Tag, PageElement, None]


# Domain.
def get_multi_movie_info(root: str, movies_list_suffix: str) -> str:
    """Gets the root path of the movie website and extracts info of first 4 movies."""
    empty_root: bool = root == "" or root is None
    empty_movies_suffix: bool = movies_list_suffix == "" or movies_list_suffix is None

    if empty_root or empty_movies_suffix:
        return ""
    if root.endswith("/"):
        root = root[:-1]
    if movies_list_suffix.endswith("/"):
        movies_list_suffix = movies_list_suffix[:-1]

    # --------------------------------------------------------
    # Extracting links to movies.
    # --------------------------------------------------------
    total_info: str = ""
    all_movies_path: str = f"{root}/{movies_list_suffix}"
    response: requests.Response = requests.get(
        all_movies_path,
        timeout=10,
    )

    res_body: str = response.text
    if response.status_code != 200:
        return "Problem with the website."

    # Unmarshaling.
    soup: BeautifulSoup = BeautifulSoup(res_body, "lxml")

    # Finding the element containing all the movies.
    main_article: UpToOneElement = soup.find(
        "article",
        class_="main-article",
    )

    if not isinstance(main_article, Tag):
        return "Problem with the website."

    anchors: ResultSet = main_article.find_all("a", href=True, limit=4)
    inner_links: list[str] = [anchor["href"] for anchor in anchors]

    # --------------------------------------------------------
    # Extracting the movies' transcripts.
    # --------------------------------------------------------

    for inner_link in inner_links:
        full_link: str = f"{root}/{inner_link}"
        movie_info: str = get_movie_info(full_link)
        total_info += f"\n\n{movie_info}"

    return total_info


# Main function.
