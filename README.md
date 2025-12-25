# BuyerScout 🔍

A SaaS-style lead generation tool that scrapes company data from Google using Selenium and enriches it with email addresses using Apollo.

## Features

- 🔎 **Google Maps Scraping**: Extract company information from Google using Selenium
- 📧 **Email Enrichment**: Enrich company data with email addresses via Apollo API (coming soon)
- 🎨 **Streamlit UI**: User-friendly web interface for managing scrapes
- 📊 **Data Export**: Export results to CSV or JSON formats

## Tech Stack

- **Python 3.10+**
- **Streamlit** - Web UI framework
- **Selenium** - Web scraping automation
- **Pandas** - Data manipulation
- **Python-dotenv** - Environment variable management

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd BuyerScout
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Apollo API key (when available)
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. The application will open in your default web browser at `http://localhost:8501`

3. Use the sidebar to configure your scraping settings:
   - Enter search query (e.g., "restaurants", "law firms")
   - Specify location (e.g., "New York, NY")
   - Set maximum number of results
   - Toggle headless mode

4. Run the scraper and view results in the main interface

## Project Structure

```
BuyerScout/
│
├── .env                  # Environment variables (not in git)
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── config.py             # Global configurations
├── app.py                # Main Streamlit application
│
├── data/                 # Data storage
│   ├── raw/              # Initial scrape results
│   └── processed/        # Enriched data
│
├── logs/                 # Application logs
│
└── src/                  # Source code
    ├── __init__.py
    ├── google_miner.py   # Google Maps scraper
    ├── apollo_enricher.py# Apollo API integration
    └── utils.py          # Utility functions
```

## Configuration

Edit `config.py` to customize:
- Selenium settings (timeouts, wait times)
- Google Maps selectors (XPATH/CSS)
- Data storage paths
- Scraping limits

## Development

### Adding New Features

1. **Google Maps Scraping**: Implement the `run_scraper()` method in `src/google_miner.py`
2. **Apollo Integration**: Implement the `enrich_company_data()` method in `src/apollo_enricher.py`
3. **UI Components**: Add new Streamlit components in `app.py`

### Logging

Logs are automatically saved to the `logs/` directory with timestamps. Use the `setup_logging()` function from `src/utils.py` to configure logging in your modules.

## TODO

- [ ] Implement Google Maps scraping logic
- [ ] Integrate Apollo API for email enrichment
- [ ] Add data validation and cleaning
- [ ] Implement pagination handling
- [ ] Add error handling and retry logic
- [ ] Create data export functionality
- [ ] Add progress tracking in UI

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

