"""
Setup script for the scraping package.
"""

from setuptools import setup, find_packages

setup(
    name="scraping",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "selenium",
        "scrapy",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "scrape=src.run.run:main",
        ]
    },
)
