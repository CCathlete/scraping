"""
Entry point to the program.
"""

import src.beautiful_soup as my_bs


def multi_movie() -> None:
    """Main funciton for this package."""
    root: str = "https://subslikescript.com"

    print()  # \n
    print(f"Root URL: {root}")
    print(f"Movie title: {my_bs.get_multi_movie_info(root)}")


def one_movie() -> None:
    """Main funciton for this package."""
    url: str = "https://subslikescript.com/movie/Taz_Quest_for_Burger-27469256"

    print()  # \n
    print(f"URL: {url}")
    print(f"Movie title: {my_bs.get_movie_info(url)}")


if __name__ == "__main__":
    multi_movie()
    # one_movie()
