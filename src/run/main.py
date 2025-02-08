"""
Entry point to the program.
"""

import src.beautiful_soup as my_bs


def one_movie() -> None:
    """Main funciton for multiple pages extraction."""
    root: str = "https://subslikescript.com/movies"

    print()  # \n
    print(f"Root URL: {root}")
    print(f"Movie title: {my_bs.get_movie_info(root)}")


def multi_movie() -> None:
    """Main funciton for single page, multiple movies
    extraction."""
    root: str = "https://subslikescript.com"
    movies_list_suffix: str = "movies"

    print()  # \n
    print(f"Root URL: {root}")
    print(f"Movie title: {my_bs.get_multi_movie_info(root, movies_list_suffix)}")


def multi_pages() -> None:
    """Main funciton for one movie extraction."""
    letter: str = "X"
    print()  # \n
    print(f"Letter: {letter}")
    print(f"Movie title: {my_bs.get_from_multi_pages(letter)}")


if __name__ == "__main__":
    multi_pages()
    # multi_movie()
    # one_movie()
