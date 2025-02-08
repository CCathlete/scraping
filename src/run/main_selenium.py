"""
Entry point to the program.
"""

import src.selenium as my_selenium


def country_matches() -> None:
    """Main funciton for a country's football matches data
    extraction."""
    country: str = "Spain"
    print()  # \n
    print(f"Country: {country}")
    print(f"Games Data: {my_selenium.get_all_matches(country)}")


if __name__ == "__main__":
    country_matches()
