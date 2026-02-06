"""
HTML parser for extracting tutorial data from Epic Games website.
"""

import logging
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class TutorialParser:
    """Parser for extracting tutorial information from HTML."""
    
    def __init__(self, base_url: str):
        """
        Initialize the parser.
        
        Args:
            base_url: Base URL for resolving relative URLs
        """
        self.base_url = base_url
    
    def parse_tutorials_page(self, html_content: str) -> List[Dict[str, Any]]:
        """
        Parse the main tutorials listing page.
        
        Args:
            html_content: HTML content of the page
            
        Returns:
            List of tutorial dictionaries
        """
        soup = BeautifulSoup(html_content, 'lxml')
        tutorials = []
        
        # Look for tutorial cards or listings
        # This will need to be adjusted based on actual page structure
        tutorial_elements = self._find_tutorial_elements(soup)
        
        for idx, element in enumerate(tutorial_elements):
            try:
                tutorial_data = self._extract_tutorial_data(element, idx)
                if tutorial_data:
                    tutorials.append(tutorial_data)
            except Exception as e:
                logger.error(f"Error parsing tutorial element: {e}")
                continue
        
        logger.info(f"Parsed {len(tutorials)} tutorials from the page")
        return tutorials
    
    def _find_tutorial_elements(self, soup: BeautifulSoup) -> List:
        """
        Find tutorial elements on the page.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            List of tutorial elements
        """
        # Try common patterns for tutorial cards
        selectors = [
            'article.tutorial',
            'div.tutorial-card',
            'div.learning-item',
            'div[class*="card"]',
            'article[class*="card"]',
            'div.resource-card',
            'a[href*="learning"]',
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                logger.info(f"Found {len(elements)} elements with selector: {selector}")
                return elements
        
        # Fallback: try to find any links in the content area
        content_area = soup.find('main') or soup.find('div', class_=re.compile('content'))
        if content_area:
            links = content_area.find_all('a', href=True)
            logger.info(f"Fallback: Found {len(links)} links in content area")
            return links
        
        logger.warning("No tutorial elements found with known selectors")
        return []
    
    def _extract_tutorial_data(self, element, index: int) -> Optional[Dict[str, Any]]:
        """
        Extract tutorial data from an element.
        
        Args:
            element: BeautifulSoup element
            index: Index for generating unique ID
            
        Returns:
            Dictionary with tutorial data or None
        """
        # Extract title
        title = self._extract_title(element)
        if not title:
            return None
        
        # Extract URL
        url = self._extract_url(element)
        if not url:
            return None
        
        # Generate unique ID from title
        tutorial_id = self._generate_id(title, index)
        
        # Extract other fields
        description = self._extract_description(element)
        category = self._extract_category(element)
        tags = self._extract_tags(element)
        author = self._extract_author(element)
        date = self._extract_date(element)
        difficulty = self._extract_difficulty(element)
        estimated_time = self._extract_time(element)
        
        return {
            "id": tutorial_id,
            "title": title,
            "description": description,
            "url": url,
            "category": category,
            "tags": tags,
            "author": author,
            "date": date,
            "difficulty": difficulty,
            "estimated_time": estimated_time,
            "scraped_at": datetime.utcnow().isoformat() + "Z"
        }
    
    def _extract_title(self, element) -> Optional[str]:
        """Extract tutorial title."""
        # Try common title patterns
        title_elem = (
            element.find('h1') or
            element.find('h2') or
            element.find('h3') or
            element.find(class_=re.compile('title', re.I)) or
            element.find(class_=re.compile('heading', re.I))
        )
        
        if title_elem:
            return title_elem.get_text(strip=True)
        
        # If element is a link, use its text
        if element.name == 'a':
            text = element.get_text(strip=True)
            if text and len(text) > 5:  # Reasonable title length
                return text
        
        return None
    
    def _extract_url(self, element) -> Optional[str]:
        """Extract tutorial URL."""
        # If element is a link
        if element.name == 'a' and element.get('href'):
            return urljoin(self.base_url, element['href'])
        
        # Look for links within element
        link = element.find('a', href=True)
        if link:
            return urljoin(self.base_url, link['href'])
        
        return None
    
    def _extract_description(self, element) -> str:
        """Extract tutorial description."""
        desc_elem = (
            element.find(class_=re.compile('description', re.I)) or
            element.find(class_=re.compile('summary', re.I)) or
            element.find('p')
        )
        
        if desc_elem:
            return desc_elem.get_text(strip=True)
        
        return ""
    
    def _extract_category(self, element) -> str:
        """Extract tutorial category."""
        category_elem = (
            element.find(class_=re.compile('category', re.I)) or
            element.find(class_=re.compile('type', re.I))
        )
        
        if category_elem:
            return category_elem.get_text(strip=True)
        
        return "General"
    
    def _extract_tags(self, element) -> List[str]:
        """Extract tutorial tags."""
        tags = []
        
        # Look for tag container
        tag_container = element.find(class_=re.compile('tag', re.I))
        if tag_container:
            tag_elements = tag_container.find_all(['span', 'a'])
            tags = [tag.get_text(strip=True) for tag in tag_elements]
        
        return [tag for tag in tags if tag]
    
    def _extract_author(self, element) -> str:
        """Extract tutorial author."""
        author_elem = (
            element.find(class_=re.compile('author', re.I)) or
            element.find(class_=re.compile('creator', re.I))
        )
        
        if author_elem:
            return author_elem.get_text(strip=True)
        
        return "Epic Games"
    
    def _extract_date(self, element) -> Optional[str]:
        """Extract publication date."""
        date_elem = (
            element.find('time') or
            element.find(class_=re.compile('date', re.I)) or
            element.find(class_=re.compile('published', re.I))
        )
        
        if date_elem:
            # Try to get datetime attribute first
            date_str = date_elem.get('datetime') or date_elem.get_text(strip=True)
            return self._normalize_date(date_str)
        
        return None
    
    def _extract_difficulty(self, element) -> Optional[str]:
        """Extract difficulty level."""
        difficulty_elem = (
            element.find(class_=re.compile('difficulty', re.I)) or
            element.find(class_=re.compile('level', re.I))
        )
        
        if difficulty_elem:
            return difficulty_elem.get_text(strip=True)
        
        return None
    
    def _extract_time(self, element) -> Optional[str]:
        """Extract estimated time."""
        time_elem = (
            element.find(class_=re.compile('duration', re.I)) or
            element.find(class_=re.compile('time', re.I))
        )
        
        if time_elem:
            return time_elem.get_text(strip=True)
        
        return None
    
    def _generate_id(self, title: str, index: int) -> str:
        """Generate unique ID from title."""
        # Create slug from title
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug[:50]  # Limit length
        return f"{slug}-{index}"
    
    def _normalize_date(self, date_str: str) -> Optional[str]:
        """Normalize date string to ISO format."""
        if not date_str:
            return None
        
        # Try to parse common date formats
        date_formats = [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
            "%B %d, %Y",
            "%b %d, %Y",
            "%d %B %Y",
            "%d %b %Y",
        ]
        
        for fmt in date_formats:
            try:
                dt = datetime.strptime(date_str.strip(), fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        
        # If parsing fails, return original
        return date_str
