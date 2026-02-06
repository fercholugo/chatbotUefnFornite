"""
Configuration settings for the Fortnite UEFN tutorial scraper.
"""

import os
from typing import Dict, Any
from pathlib import Path


class ScraperConfig:
    """Configuration class for the web scraper."""
    
    # Base URLs
    BASE_URL = "https://dev.epicgames.com/community/fortnite/learning"
    DOMAIN = "dev.epicgames.com"
    
    # Output paths
    PROJECT_ROOT = Path(__file__).parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    JSON_OUTPUT = DATA_DIR / "tutorials.json"
    MARKDOWN_DIR = DATA_DIR / "markdown"
    
    # Scraping settings
    REQUEST_TIMEOUT = 30  # seconds
    REQUEST_DELAY = 2  # seconds between requests (be respectful)
    MAX_RETRIES = 3
    RETRY_DELAY = 5  # seconds
    
    # User agents for rotation
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    
    # Export settings
    EXPORT_JSON = True
    EXPORT_MARKDOWN = True
    
    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure all required directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.MARKDOWN_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def get_headers(cls, user_agent_index: int = 0) -> Dict[str, str]:
        """Get HTTP headers with rotating user agent."""
        return {
            "User-Agent": cls.USER_AGENTS[user_agent_index % len(cls.USER_AGENTS)],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "base_url": cls.BASE_URL,
            "timeout": cls.REQUEST_TIMEOUT,
            "delay": cls.REQUEST_DELAY,
            "max_retries": cls.MAX_RETRIES,
        }
