"""
Command-line interface for the Fortnite UEFN tutorial scraper.
"""

import sys
import logging
import argparse
import json
from pathlib import Path

from scraper import TutorialScraper, ScraperConfig


def setup_logging(log_level: str = "INFO"):
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=ScraperConfig.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('scraper.log')
        ]
    )


def cmd_scrape(args):
    """Run the scraper command."""
    logger = logging.getLogger(__name__)
    logger.info("Starting scraper...")
    
    # Determine export formats
    export_json = args.format in ['json', 'all']
    export_markdown = args.format in ['markdown', 'all']
    
    # Create and run scraper
    scraper = TutorialScraper()
    
    try:
        result = scraper.run(
            export_json=export_json,
            export_markdown=export_markdown,
            update_mode=args.update
        )
        
        if result['success']:
            print(f"\n✅ Scraping completed successfully!")
            print(f"📊 Found {result['count']} tutorials")
            
            if export_json:
                print(f"📄 JSON saved to: {ScraperConfig.JSON_OUTPUT}")
            
            if export_markdown:
                print(f"📝 Markdown files saved to: {ScraperConfig.MARKDOWN_DIR}")
        else:
            print(f"\n❌ Scraping failed: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    
    finally:
        scraper.close()


def cmd_list(args):
    """List all scraped tutorials."""
    json_path = ScraperConfig.JSON_OUTPUT
    
    if not json_path.exists():
        print("❌ No tutorials found. Run 'scrape' command first.")
        sys.exit(1)
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        tutorials = data.get('tutorials', [])
        metadata = data.get('metadata', {})
        
        print(f"\n📚 Total Tutorials: {len(tutorials)}")
        print(f"🕐 Last scraped: {metadata.get('scraped_at', 'Unknown')}")
        print(f"🔗 Source: {metadata.get('source_url', 'Unknown')}\n")
        
        if args.verbose:
            # Detailed listing
            for i, tutorial in enumerate(tutorials, 1):
                print(f"{i}. {tutorial.get('title', 'Untitled')}")
                print(f"   ID: {tutorial.get('id')}")
                print(f"   URL: {tutorial.get('url')}")
                print(f"   Category: {tutorial.get('category', 'N/A')}")
                if tutorial.get('tags'):
                    print(f"   Tags: {', '.join(tutorial['tags'])}")
                print()
        else:
            # Simple listing
            for i, tutorial in enumerate(tutorials, 1):
                title = tutorial.get('title', 'Untitled')
                category = tutorial.get('category', 'N/A')
                print(f"{i}. [{category}] {title}")
    
    except Exception as e:
        print(f"❌ Error reading tutorials: {e}")
        sys.exit(1)


def cmd_search(args):
    """Search in scraped tutorials."""
    json_path = ScraperConfig.JSON_OUTPUT
    
    if not json_path.exists():
        print("❌ No tutorials found. Run 'scrape' command first.")
        sys.exit(1)
    
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        tutorials = data.get('tutorials', [])
        keyword = args.keyword.lower()
        
        # Search in title, description, and tags
        matches = []
        for tutorial in tutorials:
            title = tutorial.get('title', '').lower()
            description = tutorial.get('description', '').lower()
            tags = ' '.join(tutorial.get('tags', [])).lower()
            
            if keyword in title or keyword in description or keyword in tags:
                matches.append(tutorial)
        
        print(f"\n🔍 Found {len(matches)} tutorials matching '{args.keyword}':\n")
        
        for i, tutorial in enumerate(matches, 1):
            print(f"{i}. {tutorial.get('title', 'Untitled')}")
            print(f"   URL: {tutorial.get('url')}")
            print(f"   Category: {tutorial.get('category', 'N/A')}")
            if tutorial.get('description'):
                desc = tutorial['description'][:100]
                print(f"   Description: {desc}{'...' if len(tutorial['description']) > 100 else ''}")
            print()
    
    except Exception as e:
        print(f"❌ Error searching tutorials: {e}")
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Fortnite UEFN Tutorial Scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py scrape                    # Scrape and export to both JSON and Markdown
  python main.py scrape --format json      # Export only to JSON
  python main.py scrape --format markdown  # Export only to Markdown
  python main.py scrape --update           # Update existing data
  python main.py list                      # List all tutorials
  python main.py list --verbose            # List with details
  python main.py search "verse"            # Search for tutorials
        """
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Set logging level (default: INFO)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Scrape command
    scrape_parser = subparsers.add_parser('scrape', help='Run the web scraper')
    scrape_parser.add_argument(
        '--format',
        choices=['json', 'markdown', 'all'],
        default='all',
        help='Export format (default: all)'
    )
    scrape_parser.add_argument(
        '--update',
        action='store_true',
        help='Update existing data instead of overwriting'
    )
    scrape_parser.set_defaults(func=cmd_scrape)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all scraped tutorials')
    list_parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed information'
    )
    list_parser.set_defaults(func=cmd_list)
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search in scraped tutorials')
    search_parser.add_argument('keyword', help='Keyword to search for')
    search_parser.set_defaults(func=cmd_search)
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Execute command
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
