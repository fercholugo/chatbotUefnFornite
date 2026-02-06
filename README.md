# Fortnite UEFN Tutorial Scraper

A comprehensive Python-based web scraping solution to extract tutorial information from Epic Games' Fortnite UEFN learning resources and save it in structured formats (JSON and Markdown) for later processing.

## 🎯 Overview

This project scrapes tutorial data from [Epic Games Fortnite Learning Portal](https://dev.epicgames.com/community/fortnite/learning) and exports it in both JSON and Markdown formats. The scraped data can be used for:

- Creating a searchable knowledge base
- Building chatbots and AI assistants
- Generating consolidated guides and documentation
- Tracking learning progress
- Creating GitHub issues for learning tasks

## 📁 Project Structure

```
chatbotUefnFornite/
├── scraper/
│   ├── __init__.py         # Package initialization
│   ├── config.py           # Configuration settings
│   ├── scraper.py          # Main scraping logic
│   ├── parser.py           # HTML parsing and data extraction
│   └── exporter.py         # Data export to JSON/Markdown
├── data/
│   ├── tutorials.json      # Extracted data in JSON format
│   └── markdown/           # Individual tutorial markdown files
├── .github/
│   └── workflows/
│       └── scrape.yml      # GitHub Actions automation
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## ✨ Features

- **Robust Web Scraping**: Uses `requests` with retry logic and error handling
- **Smart HTML Parsing**: Employs BeautifulSoup4 with multiple fallback strategies
- **Rate Limiting**: Respectful scraping with configurable delays
- **User-Agent Rotation**: Mimics different browsers to avoid blocking
- **Dual Export Formats**:
  - **JSON**: Structured data for programmatic access
  - **Markdown**: Human-readable individual tutorial files
- **Update Mode**: Merge new data with existing without re-scraping
- **Search Functionality**: Search through scraped tutorials
- **Comprehensive Logging**: Debug and track scraping activities
- **CLI Interface**: Easy-to-use command-line interface

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/fercholugo/chatbotUefnFornite.git
cd chatbotUefnFornite
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage

### Basic Commands

#### Scrape Tutorials

Run the scraper to fetch and export tutorials:

```bash
# Scrape and export to both JSON and Markdown
python main.py scrape

# Export only to JSON
python main.py scrape --format json

# Export only to Markdown
python main.py scrape --format markdown

# Update existing data (merge with new tutorials)
python main.py scrape --update
```

#### List Tutorials

Display all scraped tutorials:

```bash
# Simple list
python main.py list

# Detailed list with full information
python main.py list --verbose
```

#### Search Tutorials

Search for specific keywords:

```bash
# Search for tutorials containing "verse"
python main.py search "verse"

# Search for "scripting" tutorials
python main.py search "scripting"
```

### Advanced Usage

#### Custom Log Level

```bash
python main.py --log-level DEBUG scrape
```

#### Help

```bash
# General help
python main.py --help

# Command-specific help
python main.py scrape --help
```

## 📊 Output Formats

### JSON Format

The JSON output (`data/tutorials.json`) has the following structure:

```json
{
  "tutorials": [
    {
      "id": "unique-tutorial-id",
      "title": "Tutorial Title",
      "description": "Tutorial description or summary",
      "url": "https://dev.epicgames.com/...",
      "category": "Beginner",
      "tags": ["scripting", "verse", "uefn"],
      "author": "Epic Games",
      "date": "2026-01-15",
      "difficulty": "Beginner",
      "estimated_time": "30 minutes",
      "scraped_at": "2026-02-06T10:30:00Z"
    }
  ],
  "metadata": {
    "scraped_at": "2026-02-06T10:30:00Z",
    "total_count": 50,
    "source_url": "https://dev.epicgames.com/community/fortnite/learning"
  }
}
```

### Markdown Format

Each tutorial is saved as an individual Markdown file in `data/markdown/`:

```markdown
# Tutorial Title

**Category:** Beginner  
**Difficulty:** Beginner  
**Estimated Time:** 30 minutes  
**Tags:** scripting, verse, uefn  
**Author:** Epic Games  
**Date:** 2026-01-15  
**URL:** <https://dev.epicgames.com/...>  

## Description

Tutorial description and summary goes here...

---
*Scraped at: 2026-02-06T10:30:00Z*  
*Tutorial ID: unique-tutorial-id*
```

## ⚙️ Configuration

Configuration settings can be found and modified in `scraper/config.py`:

- `BASE_URL`: Target website URL
- `REQUEST_TIMEOUT`: HTTP request timeout (30 seconds)
- `REQUEST_DELAY`: Delay between requests (2 seconds)
- `MAX_RETRIES`: Maximum retry attempts (3)
- `USER_AGENTS`: List of user agents for rotation

## 🤖 GitHub Actions Automation

The project includes a GitHub Actions workflow (`.github/workflows/scrape.yml`) that can:

- Run the scraper on a schedule (weekly by default)
- Automatically commit and push updated data
- Send notifications on failures

To enable automated scraping, ensure GitHub Actions is enabled in your repository settings.

## 🔧 Development

### Code Structure

- **`scraper/config.py`**: All configuration constants and settings
- **`scraper/scraper.py`**: Main scraper class with HTTP handling and retry logic
- **`scraper/parser.py`**: HTML parsing and data extraction logic
- **`scraper/exporter.py`**: Data export to JSON and Markdown formats
- **`main.py`**: Command-line interface and user interactions

### Logging

Logs are written to both console and `scraper.log` file. Use `--log-level` to control verbosity:

- `DEBUG`: Detailed debugging information
- `INFO`: General information (default)
- `WARNING`: Warning messages
- `ERROR`: Error messages only

## 🛡️ Best Practices

This scraper follows web scraping best practices:

1. **Respects robots.txt**: Check Epic Games' robots.txt policy
2. **Rate Limiting**: 2-second delay between requests (configurable)
3. **User-Agent Rotation**: Mimics real browsers
4. **Error Handling**: Comprehensive try-except blocks
5. **Retry Logic**: Automatic retries with exponential backoff
6. **Logging**: Full activity logging for debugging

## 🐛 Troubleshooting

### No tutorials found

- Check if the website structure has changed
- Try increasing `REQUEST_TIMEOUT` in `config.py`
- Enable DEBUG logging: `python main.py --log-level DEBUG scrape`

### Connection errors

- Check your internet connection
- Verify the target URL is accessible
- Check if you're behind a proxy or firewall

### Import errors

- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using Python 3.9 or higher: `python --version`

## 🚀 Future Enhancements

Potential improvements and extensions:

- [ ] Support for JavaScript-rendered content (Selenium/Playwright)
- [ ] Incremental updates with change detection
- [ ] Database storage option (SQLite, PostgreSQL)
- [ ] REST API for accessing scraped data
- [ ] Docker containerization
- [ ] Tutorial content extraction (not just metadata)
- [ ] Image and asset downloading
- [ ] Integration with chatbot frameworks
- [ ] Analytics and statistics dashboard
- [ ] Multi-language support

## 📝 License

This project is provided as-is for educational and research purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Contact

For questions or support, please open an issue on GitHub.

## ⚠️ Disclaimer

This tool is for educational purposes only. Always respect the website's terms of service and robots.txt policy. Epic Games owns all content from their website.

---

**Happy Scraping! 🎮**