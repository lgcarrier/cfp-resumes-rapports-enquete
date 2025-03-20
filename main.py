import requests
from bs4 import BeautifulSoup
import os
from fake_useragent import UserAgent
import logging
from urllib.parse import urljoin
import argparse
import json
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('resumes_rapports_enquete.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize UserAgent for random browser/device mimicking
ua = UserAgent()

# Base URL for the investigation summaries
BASE_URL = "https://www.cfp.gouv.qc.ca/fr/documentation/resumes-denquete.html"

# Directory to save investigation summaries
OUTPUT_DIR = "resumes_rapports_enquete"
os.makedirs(OUTPUT_DIR, exist_ok=True)

### Utility Functions

def get_random_headers():
    """Generate random headers with different User-Agent."""
    return {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive"
    }

def sanitize_filename(filename):
    """Remove invalid characters from filename and limit length."""
    return re.sub(r'[^\w\-_\. ]', '_', filename)

### Scraping Functions

def get_year_links(soup):
    """
    Extract links to investigation pages for each year from the main page.
    
    Returns:
        List of tuples (year_text, year_url) where year_text is the year (e.g., '2025')
        and year_url is the full URL to that year's investigations page.
    """
    left_col = soup.select_one("div.leftColonne")
    if not left_col:
        logger.debug("No left column found on main page")
        return []
    
    year_items = left_col.select("li.nav-item a")
    links = []
    for item in year_items:
        year_text = item.get_text(strip=True)
        if year_text != "Dossiers d'intérêt publiés dans les rapports annuels de 2009 à 2014":
            if href := item.get('href'):
                full_url = urljoin(BASE_URL, href)
                links.append((year_text, full_url))
                logger.debug(f"Found year link: {year_text} -> {full_url}")
    logger.debug(f"Found {len(links)} year links")
    return links

def extract_investigation(item):
    """
    Extract title and content from an investigation item.
    
    Args:
        item: BeautifulSoup object representing a div.item blog post.
    
    Returns:
        Dictionary with 'title' and 'content' keys.
    """
    title = item.select_one('h2').get_text(strip=True) if item.select_one('h2') else "No title"
    content_div = item.select_one('div.item-intro')
    if content_div:
        content = content_div.get_text(separator='\n', strip=True)
    else:
        content = "No content"
    return {'title': title, 'content': content}

def scrape_year(year_url):
    """
    Scrape all investigations from a year's page, handling pagination.
    
    Args:
        year_url: URL of the year's investigation page.
    
    Returns:
        List of dictionaries, each containing 'title' and 'content' for an investigation.
    """
    investigations = []
    current_url = year_url
    
    while current_url:
        headers = get_random_headers()
        try:
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch {current_url}: {e}")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract investigations from the current page
        items = soup.select("div.com-content-category-blog__items.blog-items div.item")
        for item in items:
            investigation = extract_investigation(item)
            if investigation:
                investigations.append(investigation)
        
        # Check for next page in pagination
        next_link = soup.select_one('ul.pagination a[aria-label="Aller à la page suivant"]')
        if next_link and 'href' in next_link.attrs:
            current_url = urljoin(current_url, next_link['href'])
        else:
            current_url = None
    
    logger.debug(f"Scraped {len(investigations)} investigations from {year_url}")
    return investigations

def save_to_json(data, filepath):
    """Save data to a JSON file with proper encoding."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logger.info(f"Saved investigations to {filepath}")

### Main Function

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Scrape investigation summaries from CFP Quebec')
    parser.add_argument('--year', type=str, help='Scrape investigations for a specific year (e.g., 2025)')
    args = parser.parse_args()
    
    logger.info("Starting investigation summaries scraping process")
    
    # Fetch the main page
    headers = get_random_headers()
    try:
        response = requests.get(BASE_URL, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch main page {BASE_URL}: {e}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Get links to each year's investigation page
    year_links = get_year_links(soup)
    if not year_links:
        logger.warning("No year links found on the main page")
        return
    
    # Filter by specific year if provided
    if args.year:
        year_links = [link for link in year_links if args.year in link[0]]
        if not year_links:
            logger.error(f"No investigations found for year {args.year}")
            return
    
    # Process each year
    for year_text, year_url in year_links:
        try:
            logger.info(f"Scraping investigations for year {year_text}")
            investigations = scrape_year(year_url)
            
            # Create a directory for the year
            year_dir = os.path.join(OUTPUT_DIR, year_text)
            os.makedirs(year_dir, exist_ok=True)

            # Save as JSON
            filename = f"{sanitize_filename(year_text)}.json"
            filepath = os.path.join(year_dir, filename)
            save_to_json(investigations, filepath)
            
        except Exception as e:
            logger.error(f"Error processing year {year_text}: {e}", exc_info=True)
    
    logger.info("Investigation summaries scraping process completed")

if __name__ == "__main__":
    main()