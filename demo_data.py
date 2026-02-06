"""
Demo script to populate the data directory with sample tutorials.

This script can be used to test the scraper functionality when the actual
Epic Games website is not accessible (e.g., in restricted environments).

Usage:
    python demo_data.py
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from scraper.exporter import DataExporter
from scraper.config import ScraperConfig


def create_sample_data():
    """Create sample tutorial data for demonstration."""
    
    sample_tutorials = [
        {
            "id": "getting-started-with-uefn-0",
            "title": "Getting Started with UEFN",
            "description": "Learn the basics of Unreal Editor for Fortnite (UEFN). This comprehensive tutorial will guide you through the initial setup and core concepts.",
            "url": "https://dev.epicgames.com/community/fortnite/learning/getting-started",
            "category": "Beginner",
            "tags": ["uefn", "basics", "getting-started"],
            "author": "Epic Games",
            "date": "2024-01-15",
            "difficulty": "Beginner",
            "estimated_time": "30 minutes",
            "scraped_at": "2026-02-06T23:30:00Z"
        },
        {
            "id": "intro-to-verse-scripting-1",
            "title": "Introduction to Verse Scripting",
            "description": "Master the fundamentals of Verse, Epic's programming language for UEFN. Learn syntax, data types, and basic scripting concepts.",
            "url": "https://dev.epicgames.com/community/fortnite/learning/verse-intro",
            "category": "Intermediate",
            "tags": ["verse", "scripting", "programming"],
            "author": "Epic Games",
            "date": "2024-02-01",
            "difficulty": "Intermediate",
            "estimated_time": "1 hour",
            "scraped_at": "2026-02-06T23:30:00Z"
        },
        {
            "id": "building-custom-devices-2",
            "title": "Building Custom Devices in UEFN",
            "description": "Create your own custom devices and game mechanics using UEFN's powerful device system.",
            "url": "https://dev.epicgames.com/community/fortnite/learning/custom-devices",
            "category": "Advanced",
            "tags": ["devices", "gameplay", "mechanics"],
            "author": "Epic Games",
            "date": "2024-03-10",
            "difficulty": "Advanced",
            "estimated_time": "2 hours",
            "scraped_at": "2026-02-06T23:30:00Z"
        },
        {
            "id": "level-design-basics-3",
            "title": "Level Design Basics for UEFN",
            "description": "Learn how to design engaging game levels in UEFN. Covers layout, flow, and player experience principles.",
            "url": "https://dev.epicgames.com/community/fortnite/learning/level-design",
            "category": "Beginner",
            "tags": ["level-design", "world-building", "environment"],
            "author": "Epic Games",
            "date": "2024-01-20",
            "difficulty": "Beginner",
            "estimated_time": "45 minutes",
            "scraped_at": "2026-02-06T23:30:00Z"
        },
        {
            "id": "advanced-verse-patterns-4",
            "title": "Advanced Verse Programming Patterns",
            "description": "Explore advanced programming patterns and best practices in Verse for creating complex game systems.",
            "url": "https://dev.epicgames.com/community/fortnite/learning/verse-advanced",
            "category": "Advanced",
            "tags": ["verse", "programming", "patterns", "advanced"],
            "author": "Epic Games",
            "date": "2024-03-01",
            "difficulty": "Advanced",
            "estimated_time": "2.5 hours",
            "scraped_at": "2026-02-06T23:30:00Z"
        }
    ]
    
    return sample_tutorials


def main():
    """Main function to create demo data."""
    
    print("🎮 Fortnite UEFN Tutorial Scraper - Demo Data Generator")
    print("=" * 60)
    print()
    
    # Ensure directories exist
    ScraperConfig.ensure_directories()
    
    # Create sample data
    tutorials = create_sample_data()
    
    print(f"📝 Creating {len(tutorials)} sample tutorials...")
    
    # Create exporter
    exporter = DataExporter(
        ScraperConfig.JSON_OUTPUT,
        ScraperConfig.MARKDOWN_DIR
    )
    
    # Export data
    metadata = {
        "source_url": ScraperConfig.BASE_URL,
        "total_count": len(tutorials),
        "note": "This is demo/sample data for testing purposes"
    }
    
    exporter.export_all(
        tutorials,
        export_json=True,
        export_markdown=True,
        metadata=metadata
    )
    
    print()
    print("✅ Demo data created successfully!")
    print()
    print(f"📄 JSON file: {ScraperConfig.JSON_OUTPUT}")
    print(f"📝 Markdown directory: {ScraperConfig.MARKDOWN_DIR}")
    print()
    print("🔍 You can now test the CLI commands:")
    print("  python main.py list")
    print("  python main.py list --verbose")
    print("  python main.py search verse")
    print("  python main.py search beginner")
    print()


if __name__ == "__main__":
    main()
