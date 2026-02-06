"""
Fortnite UEFN Tutorial Scraper Package

A Python-based web scraping solution to extract tutorial information
from Epic Games' Fortnite UEFN learning resources.
"""

__version__ = "1.0.0"
__author__ = "Fortnite UEFN Bot Team"

from .scraper import TutorialScraper
from .parser import TutorialParser
from .exporter import DataExporter
from .config import ScraperConfig

__all__ = ["TutorialScraper", "TutorialParser", "DataExporter", "ScraperConfig"]
