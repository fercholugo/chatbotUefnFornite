# Usage Demonstration

This document demonstrates the complete functionality of the Fortnite UEFN Tutorial Scraper.

## Installation

```bash
# Clone the repository
git clone https://github.com/fercholugo/chatbotUefnFornite.git
cd chatbotUefnFornite

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Generate Demo Data (for testing)

```bash
$ python demo_data.py
🎮 Fortnite UEFN Tutorial Scraper - Demo Data Generator
============================================================

📝 Creating 5 sample tutorials...

✅ Demo data created successfully!

📄 JSON file: /path/to/data/tutorials.json
📝 Markdown directory: /path/to/data/markdown
```

### 2. List All Tutorials

```bash
$ python main.py list
📚 Total Tutorials: 5
🕐 Last scraped: 2026-02-06T23:32:36.952478Z
🔗 Source: https://dev.epicgames.com/community/fortnite/learning

1. [Beginner] Getting Started with UEFN
2. [Intermediate] Introduction to Verse Scripting
3. [Advanced] Building Custom Devices in UEFN
4. [Beginner] Level Design Basics for UEFN
5. [Advanced] Advanced Verse Programming Patterns
```

### 3. List with Verbose Details

```bash
$ python main.py list --verbose
📚 Total Tutorials: 5
🕐 Last scraped: 2026-02-06T23:32:36.952478Z
🔗 Source: https://dev.epicgames.com/community/fortnite/learning

1. Getting Started with UEFN
   ID: getting-started-with-uefn-0
   URL: https://dev.epicgames.com/community/fortnite/learning/getting-started
   Category: Beginner
   Tags: uefn, basics, getting-started

2. Introduction to Verse Scripting
   ID: intro-to-verse-scripting-1
   URL: https://dev.epicgames.com/community/fortnite/learning/verse-intro
   Category: Intermediate
   Tags: verse, scripting, programming
...
```

### 4. Search for Tutorials

```bash
$ python main.py search "verse"
🔍 Found 2 tutorials matching 'verse':

1. Introduction to Verse Scripting
   URL: https://dev.epicgames.com/community/fortnite/learning/verse-intro
   Category: Intermediate
   Description: Master the fundamentals of Verse, Epic's programming language...

2. Advanced Verse Programming Patterns
   URL: https://dev.epicgames.com/community/fortnite/learning/verse-advanced
   Category: Advanced
   Description: Explore advanced programming patterns and best practices...
```

### 5. Run the Scraper (requires internet access)

```bash
$ python main.py scrape
2026-02-06 23:31:28,908 - __main__ - INFO - Starting scraper...
2026-02-06 23:31:28,908 - scraper.scraper - INFO - Starting scrape from https://dev.epicgames.com/community/fortnite/learning
...

✅ Scraping completed successfully!
📊 Found 50 tutorials
📄 JSON saved to: /path/to/data/tutorials.json
📝 Markdown files saved to: /path/to/data/markdown
```

### 6. Export Options

```bash
# Export only to JSON
$ python main.py scrape --format json

# Export only to Markdown
$ python main.py scrape --format markdown

# Update existing data (merge new with old)
$ python main.py scrape --update
```

## Output Examples

### JSON Output (data/tutorials.json)

```json
{
  "tutorials": [
    {
      "id": "getting-started-with-uefn-0",
      "title": "Getting Started with UEFN",
      "description": "Learn the basics of Unreal Editor for Fortnite...",
      "url": "https://dev.epicgames.com/community/fortnite/learning/getting-started",
      "category": "Beginner",
      "tags": ["uefn", "basics", "getting-started"],
      "author": "Epic Games",
      "date": "2024-01-15",
      "difficulty": "Beginner",
      "estimated_time": "30 minutes",
      "scraped_at": "2026-02-06T23:30:00Z"
    }
  ],
  "metadata": {
    "scraped_at": "2026-02-06T23:31:52.005063Z",
    "total_count": 5,
    "source_url": "https://dev.epicgames.com/community/fortnite/learning"
  }
}
```

### Markdown Output (data/markdown/intro-to-verse-scripting-1.md)

```markdown
# Introduction to Verse Scripting

**Category:** Intermediate  
**Difficulty:** Intermediate  
**Estimated Time:** 1 hour  
**Tags:** verse, scripting, programming  
**Author:** Epic Games  
**Date:** 2024-02-01  
**URL:** <https://dev.epicgames.com/community/fortnite/learning/verse-intro>  

## Description

Master the fundamentals of Verse, Epic's programming language for UEFN...

---

*Scraped at: 2026-02-06T23:30:00Z*  
*Tutorial ID: intro-to-verse-scripting-1*
```

## Advanced Usage

### Custom Log Level

```bash
$ python main.py --log-level DEBUG scrape
# Shows detailed debugging information
```

### Help Commands

```bash
$ python main.py --help
$ python main.py scrape --help
$ python main.py list --help
$ python main.py search --help
```

## GitHub Actions Automation

The project includes a GitHub Actions workflow that:
- Runs weekly on Mondays at 9 AM UTC
- Scrapes the latest tutorials
- Commits and pushes updated data
- Can be triggered manually

## Tips

1. **Rate Limiting**: The scraper includes a 2-second delay between requests to be respectful to the server.

2. **Error Handling**: All errors are logged to `scraper.log` for debugging.

3. **Update Mode**: Use `--update` to merge new tutorials with existing data without losing manual edits.

4. **Demo Data**: Use `demo_data.py` when testing in environments without internet access.

5. **Search**: Search is case-insensitive for title, description, and tags.

## Troubleshooting

### No tutorials found
- Enable DEBUG logging: `python main.py --log-level DEBUG scrape`
- Check network connectivity
- Verify the target URL is accessible

### Import errors
- Ensure dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (requires 3.9+)

### JSON validation error
- The JSON file may be corrupted
- Delete and re-run the scraper
- Check `scraper.log` for details

---

**Ready to scrape! 🎮**
