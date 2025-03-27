import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from constants import HOTMART_BLOG_URL

class ScraperException(Exception):
    """Custom exception for scraper-related errors"""
    pass

def scrape_content():
    """
    Scrape content from a Hotmart blog post URL and extract relevant text elements.
    
    Returns:
        str: Formatted text content from the page.
        
    Raises:
        ScraperException: If there's an error during scraping or content processing
        RequestException: If there's an error with the HTTP request
    """
    try:
        # Handle network-related errors
        try:
            response = requests.get(HOTMART_BLOG_URL, timeout=10)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
        except RequestException as e:
            raise ScraperException(f"Failed to fetch content: {str(e)}")
        
        # Handle parsing errors
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            raise ScraperException(f"Failed to parse HTML content: {str(e)}")
        
        # Find main content
        content_body = soup.find('div', class_='content__body')
        if not content_body:
            print("Warning: Default main content not found, using fallback content (every paragraph will be included)")
            content_body = BeautifulSoup('<div></div>', 'html.parser')
            paragraphs = soup.find_all('p')
            if not paragraphs:
                raise ScraperException("No content found in the page")
            for p in paragraphs:
                content_body.div.append(p)
        
        # Extract relevant content
        extracted_text = []
        relevant_content = content_body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li'])
        
        if not relevant_content:
            raise ScraperException("No relevant content found in the page")
        
        for element in relevant_content:
            if element.name == 'li' and element.find_parent('li'):
                continue
                
            if element.name == 'p' and element.find_parent(['li', 'div.text', 'span.text']):
                continue
                
            text = element.get_text().strip()
            if not text:
                continue
                
            if element.name.startswith('h'):
                extracted_text.append(f"\n\n{text}\n")
            elif element.name == 'li':
                extracted_text.append(f"\n{text}")
            else:
                extracted_text.append(f"{text}\n")
        
        final_text = ''.join(extracted_text)
        if not final_text.strip():
            raise ScraperException("Extracted content is empty")
            
        return final_text
        
    except ScraperException:
        raise
    except Exception as e:
        raise ScraperException(f"Unexpected error during content scraping: {str(e)}")
