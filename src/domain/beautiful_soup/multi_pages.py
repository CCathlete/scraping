"""
Getting movie info spanning over multiple pages.
"""

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
from src.domain.beautiful_soup.multi_movie import get_multi_movie_info

# Helpers.
UpToOneElement: TypeAlias = Union[Tag, PageElement, None]


# Domain.
def get_from_multi_pages(letter: str) -> str:
    """Gets root URL and a letter and returns the info of all movies starting with this letter."""

    # We split the url to multiple parts to first get the list
    # of link to movies and then handle a get request for each
    # movie.
    root: str = "https://subslikescript.com"
    movie_suffix: str = f"movies_letter-{letter}"
    # The complete url for all movies starting withe the given letter.
    url: str = f"{root}/{movie_suffix}"

    response: requests.Response = requests.get(
        url,
        timeout=10,
    )
    body: str = response.text

    # Unmarshaling = parsing html into a python object.
    soup: BeautifulSoup = BeautifulSoup(body, "lxml")
    # Extracting the pagination element from the HTML.
    pagination_element: UpToOneElement = soup.find(
        "ul",
        class_="pagination",
    )

    if not isinstance(pagination_element, Tag):
        return "Didn't find a pagination element."

    # Extracting all list items from the pagination element.
    pages: ResultSet = pagination_element.find_all(
        "li",
        class_="page-item",
    )
    # pages[-1], the last element of pages is an <li> with the
    # "next" button. So the actual last page is pages[-2].
    # Pages contain HTML Tag elements so we need to extract
    # the text using the Tag.text method.
    last_page: int = int(pages[-2].text)
    first_page: int = 1  # pages[0] is a "previous" button.

    # Extracting info of multiple movies from each page.
    # We want to include the last page so stop condition is
    # last_page + 1.
    total_info: str = ""
    for page in range(first_page, last_page + 1):
        page_suffix: str = f"{movie_suffix}?page={page}"
        total_info += (
            f"\n\n\nPage: {page}" + f"{get_multi_movie_info(root, page_suffix)}"
        )

    return total_info
