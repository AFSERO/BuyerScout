"""
Global configuration file for BuyerScout.
Contains constants, XPATH selectors, and configuration settings.
"""

from typing import Dict


class Config:
    """Configuration class for BuyerScout application."""
    
    # Selenium Settings
    HEADLESS_MODE: bool = False
    IMPLICIT_WAIT: int = 10  # seconds
    PAGE_LOAD_TIMEOUT: int = 30  # seconds
    
    # Google Maps Selectors (XPATH/CSS)
    GOOGLE_MAPS_SELECTORS: Dict[str, str] = {
        # TODO: Add actual selectors after inspecting Google Maps structure
        'search_box': '//input[@id="searchboxinput"]',
        'search_button': '//button[@id="searchbox-searchbutton"]',
        'business_name': '//h1[contains(@class, "DUwDvf")]',
        'address': '//button[@data-item-id="address"]',
        'phone': '//button[contains(@data-value, "phone")]',
        'website': '//a[contains(@data-value, "website")]',
        'rating': '//div[contains(@class, "F7nice")]',
        'reviews_count': '//span[contains(@class, "DkEaL")]',
        'business_listing': '//div[contains(@class, "Nv2PK")]',
        'next_page_button': '//button[@aria-label="Next"]',
    }
    
    # Apollo API Settings (for future use)
    APOLLO_API_BASE_URL: str = "https://api.apollo.io/v1"
    APOLLO_API_KEY: str = ""  # Set via .env file
    
    # Data Storage Paths
    DATA_RAW_PATH: str = "data/raw"
    DATA_PROCESSED_PATH: str = "data/processed"
    LOGS_PATH: str = "logs"
    
    # Scraping Settings
    MAX_RESULTS_PER_SEARCH: int = 100
    DELAY_BETWEEN_REQUESTS: float = 2.0  # seconds
    SCROLL_PAUSE_TIME: float = 2.0  # seconds


# Create a singleton instance
config = Config()

