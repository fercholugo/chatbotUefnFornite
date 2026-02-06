"""
Main web scraper for Fortnite UEFN tutorials.
"""

import logging
import time
import requests
from typing import List, Dict, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import ScraperConfig
from .parser import TutorialParser
from .exporter import DataExporter

logger = logging.getLogger(__name__)


class TutorialScraper:
    """Web scraper for Fortnite UEFN tutorials."""
    
    def __init__(self, config: ScraperConfig = None):
        """
        Initialize the scraper.
        
        Args:
            config: Configuration object (uses default if None)
        """
        self.config = config or ScraperConfig()
        self.parser = TutorialParser(self.config.BASE_URL)
        self.exporter = DataExporter(
            self.config.JSON_OUTPUT,
            self.config.MARKDOWN_DIR
        )
        self.session = self._create_session()
        self.request_count = 0
    
    def _create_session(self) -> requests.Session:
        """
        Create a requests session with retry logic.
        
        Returns:
            Configured requests session
        """
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.config.MAX_RETRIES,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with rotating user agent."""
        return self.config.get_headers(self.request_count)
    
    def _fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a web page with error handling and rate limiting.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None on error
        """
        try:
            # Rate limiting
            if self.request_count > 0:
                logger.debug(f"Waiting {self.config.REQUEST_DELAY}s before next request")
                time.sleep(self.config.REQUEST_DELAY)
            
            logger.info(f"Fetching: {url}")
            
            response = self.session.get(
                url,
                headers=self._get_headers(),
                timeout=self.config.REQUEST_TIMEOUT
            )
            
            response.raise_for_status()
            self.request_count += 1
            
            logger.info(f"Successfully fetched {url} (status: {response.status_code})")
            return response.text
            
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def scrape_tutorials(self) -> List[Dict[str, Any]]:
        """
        Scrape tutorials from the main page.
        
        Returns:
            List of tutorial dictionaries
        """
        logger.info(f"Starting scrape from {self.config.BASE_URL}")
        
        # Fetch main page
        html_content = self._fetch_page(self.config.BASE_URL)
        if not html_content:
            logger.error("Failed to fetch main page")
            return []
        
        # Parse tutorials
        tutorials = self.parser.parse_tutorials_page(html_content)
        
        if not tutorials:
            logger.warning("No tutorials found on the page")
        
        return tutorials
    
    def run(self, export_json: bool = True, export_markdown: bool = True,
            update_mode: bool = False) -> Dict[str, Any]:
        """
        Run the complete scraping pipeline.
        
        Args:
            export_json: Whether to export to JSON
            export_markdown: Whether to export to Markdown
            update_mode: Whether to merge with existing data
            
        Returns:
            Dictionary with scraping results and statistics
        """
        try:
            # Ensure output directories exist
            self.config.ensure_directories()
            
            # Scrape tutorials
            tutorials = self.scrape_tutorials()
            
            if not tutorials:
                return {
                    "success": False,
                    "error": "No tutorials found",
                    "count": 0
                }
            
            # Handle update mode
            if update_mode:
                existing_tutorials = self.exporter.load_existing_json()
                tutorials = self._merge_tutorials(existing_tutorials, tutorials)
            
            # Prepare metadata
            metadata = {
                "source_url": self.config.BASE_URL,
                "scraper_config": self.config.to_dict(),
                "total_count": len(tutorials),
            }
            
            # Export data
            self.exporter.export_all(
                tutorials,
                export_json=export_json,
                export_markdown=export_markdown,
                metadata=metadata
            )
            
            logger.info(f"Scraping completed successfully. Found {len(tutorials)} tutorials")
            
            return {
                "success": True,
                "count": len(tutorials),
                "tutorials": tutorials,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Error during scraping: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "count": 0
            }
    
    def _merge_tutorials(self, existing: List[Dict[str, Any]], 
                        new: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Merge existing and new tutorials, avoiding duplicates.
        
        Args:
            existing: List of existing tutorials
            new: List of newly scraped tutorials
            
        Returns:
            Merged list of tutorials
        """
        # Create a map of existing tutorials by URL
        existing_map = {t['url']: t for t in existing if 'url' in t}
        
        # Update with new tutorials
        for tutorial in new:
            url = tutorial.get('url')
            if url:
                existing_map[url] = tutorial
        
        merged = list(existing_map.values())
        logger.info(f"Merged tutorials: {len(existing)} existing + {len(new)} new = {len(merged)} total")
        
        return merged
    
    def close(self):
        """Close the scraper session."""
        if self.session:
            self.session.close()
            logger.info("Scraper session closed")
