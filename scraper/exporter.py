"""
Data exporter for saving tutorial data in JSON and Markdown formats.
"""

import json
import logging
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class DataExporter:
    """Exporter for tutorial data to JSON and Markdown formats."""
    
    def __init__(self, json_path: Path, markdown_dir: Path):
        """
        Initialize the exporter.
        
        Args:
            json_path: Path to JSON output file
            markdown_dir: Directory for markdown files
        """
        self.json_path = json_path
        self.markdown_dir = markdown_dir
    
    def export_json(self, tutorials: List[Dict[str, Any]], metadata: Dict[str, Any] = None) -> None:
        """
        Export tutorials to JSON format.
        
        Args:
            tutorials: List of tutorial dictionaries
            metadata: Optional metadata to include
        """
        if metadata is None:
            metadata = {}
        
        # Add default metadata
        metadata.update({
            "scraped_at": datetime.utcnow().isoformat() + "Z",
            "total_count": len(tutorials),
        })
        
        output_data = {
            "tutorials": tutorials,
            "metadata": metadata
        }
        
        try:
            # Ensure parent directory exists
            self.json_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write JSON file with pretty printing
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Exported {len(tutorials)} tutorials to {self.json_path}")
        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            raise
    
    def export_markdown(self, tutorials: List[Dict[str, Any]]) -> None:
        """
        Export tutorials to individual Markdown files.
        
        Args:
            tutorials: List of tutorial dictionaries
        """
        try:
            # Ensure markdown directory exists
            self.markdown_dir.mkdir(parents=True, exist_ok=True)
            
            for tutorial in tutorials:
                self._export_single_markdown(tutorial)
            
            logger.info(f"Exported {len(tutorials)} tutorials to {self.markdown_dir}")
        except Exception as e:
            logger.error(f"Error exporting to Markdown: {e}")
            raise
    
    def _export_single_markdown(self, tutorial: Dict[str, Any]) -> None:
        """
        Export a single tutorial to Markdown format.
        
        Args:
            tutorial: Tutorial dictionary
        """
        tutorial_id = tutorial.get('id', 'unknown')
        filename = f"{tutorial_id}.md"
        filepath = self.markdown_dir / filename
        
        # Build markdown content
        content = self._build_markdown_content(tutorial)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Error writing markdown file {filepath}: {e}")
            raise
    
    def _build_markdown_content(self, tutorial: Dict[str, Any]) -> str:
        """
        Build markdown content for a tutorial.
        
        Args:
            tutorial: Tutorial dictionary
            
        Returns:
            Markdown formatted string
        """
        lines = []
        
        # Title
        title = tutorial.get('title', 'Untitled')
        lines.append(f"# {title}\n")
        
        # Metadata section
        if tutorial.get('category'):
            lines.append(f"**Category:** {tutorial['category']}  ")
        
        if tutorial.get('difficulty'):
            lines.append(f"**Difficulty:** {tutorial['difficulty']}  ")
        
        if tutorial.get('estimated_time'):
            lines.append(f"**Estimated Time:** {tutorial['estimated_time']}  ")
        
        if tutorial.get('tags'):
            tags_str = ", ".join(tutorial['tags'])
            lines.append(f"**Tags:** {tags_str}  ")
        
        if tutorial.get('author'):
            lines.append(f"**Author:** {tutorial['author']}  ")
        
        if tutorial.get('date'):
            lines.append(f"**Date:** {tutorial['date']}  ")
        
        if tutorial.get('url'):
            lines.append(f"**URL:** <{tutorial['url']}>  ")
        
        lines.append("")
        
        # Description section
        if tutorial.get('description'):
            lines.append("## Description\n")
            lines.append(f"{tutorial['description']}\n")
        
        # Additional sections can be added here
        # For example, prerequisites, resources, etc.
        
        # Footer with scraping metadata
        lines.append("---\n")
        lines.append(f"*Scraped at: {tutorial.get('scraped_at', 'Unknown')}*  ")
        lines.append(f"*Tutorial ID: {tutorial.get('id', 'Unknown')}*")
        
        return "\n".join(lines)
    
    def export_all(self, tutorials: List[Dict[str, Any]], export_json: bool = True, 
                   export_markdown: bool = True, metadata: Dict[str, Any] = None) -> None:
        """
        Export tutorials to all enabled formats.
        
        Args:
            tutorials: List of tutorial dictionaries
            export_json: Whether to export JSON
            export_markdown: Whether to export Markdown
            metadata: Optional metadata for JSON export
        """
        if export_json:
            self.export_json(tutorials, metadata)
        
        if export_markdown:
            self.export_markdown(tutorials)
    
    def load_existing_json(self) -> List[Dict[str, Any]]:
        """
        Load existing tutorials from JSON file.
        
        Returns:
            List of existing tutorials or empty list
        """
        if not self.json_path.exists():
            return []
        
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            tutorials = data.get('tutorials', [])
            logger.info(f"Loaded {len(tutorials)} existing tutorials from {self.json_path}")
            return tutorials
        except Exception as e:
            logger.error(f"Error loading existing JSON: {e}")
            return []
