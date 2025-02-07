"""Scraping data of a single movie from subslikescript.com """

from typing import Union
from bs4 import BeautifulSoup
from bs4.element import (
    Tag,
    PageElement,
)
import requests
from typing_extensions import TypeAlias

UpToOneElement: TypeAlias = Union[Tag, PageElement, None]


def get_movie_title(url: str) -> str:
    """Gets a url for a movie in sublikescript.com and returns
    the movie's title.
    """

    title: str = ""
    response: requests.Response = requests.get(
        url,
        timeout=10,
    )

    # Response's body, HTML in this case.
    content: str = response.text
    # Using the lxml html/xml parser.
    soup: BeautifulSoup = BeautifulSoup(content, "lxml")
    # Printing the soup.
    # print(soup.prettify)

    # Finding the article tag in HTML, it has the title and
    # transcript inside.
    article_element: UpToOneElement = soup.find(
        "article",
        class_="main-article",
    )

    if isinstance(article_element, Tag):
        h1_tag: UpToOneElement = article_element.find("h1")
        if h1_tag:
            title = h1_tag.get_text()

    return title


def main() -> None:
    """Main funciton for this package."""
    url: str = "https://subslikescript.com/movie/Titanic-120338"

    print()  # \n
    print(f"URL: {url}")
    print(f"Movie title: {get_movie_title(url)}")


if __name__ == "__main__":
    main()
