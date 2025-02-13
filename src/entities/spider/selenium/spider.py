"""
Selenium based implementation of the spider.Skeleton 
interface.
"""

from src.entities.spider.interface import Skeleton


class Spider(Skeleton):
    """A spider that uses Selenium to scrape data."""
