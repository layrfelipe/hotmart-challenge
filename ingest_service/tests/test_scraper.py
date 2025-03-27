import pytest
import sys
from pathlib import Path
from unittest.mock import patch, Mock
from requests.exceptions import RequestException

#sys.path.append(str(Path(__file__).parent.parent))
from scraper import scrape_content, ScraperException

@pytest.fixture
def mock_html():
    return """
    <html>
        <body>
            <div class="content__body">
                <h1>Test Header</h1>
                <p>Test paragraph 1</p>
                <ul>
                    <li>List item 1</li>
                    <li>List item 2</li>
                </ul>
                <h2>Second Header</h2>
                <p>Test paragraph 2</p>
            </div>
        </body>
    </html>
    """

def test_scrape_content_success(mock_html):
    """Test successful content scraping with proper HTML structure"""
    with patch('scraper.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = mock_html
        mock_get.return_value = mock_response
        
        result = scrape_content()
        
        assert "Test Header" in result
        assert "Test paragraph 1" in result
        assert "List item 1" in result
        assert "List item 2" in result
        assert "Second Header" in result
        assert "Test paragraph 2" in result
        
        mock_get.assert_called_once_with(
            "https://hotmart.com/pt-br/blog/como-funciona-hotmart",
            timeout=10
        )
        print("\n✓ Content scraping test passed: all expected content found")

def test_scrape_content_no_content_body(mock_html):
    """Test fallback behavior when content__body class is not found"""
    modified_html = mock_html.replace('content__body', 'wrong-class')
    
    with patch('scraper.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = modified_html
        mock_get.return_value = mock_response
        
        result = scrape_content()
        
        assert "Test paragraph 1" in result
        assert "Test paragraph 2" in result
        print("\n✓ Fallback scraping test passed: paragraphs found without content__body")

def test_scrape_content_network_error():
    """Test handling of network errors"""
    with patch('scraper.requests.get') as mock_get:
        mock_get.side_effect = RequestException("Network error")
        
        with pytest.raises(ScraperException) as exc_info:
            scrape_content()
        
        assert "Failed to fetch content" in str(exc_info.value)
        assert "Network error" in str(exc_info.value)
        print("\n✓ Network error test passed: correctly handled exception")

def test_scrape_content_http_error():
    """Test handling of HTTP errors"""
    with patch('scraper.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = RequestException("404 Client Error")
        mock_get.return_value = mock_response
        
        with pytest.raises(ScraperException) as exc_info:
            scrape_content()
        
        assert "Failed to fetch content" in str(exc_info.value)
        print("\n✓ HTTP error test passed: correctly handled status code error")

def test_scrape_content_empty_response():
    """Test handling of empty HTML response"""
    with patch('scraper.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = "<html><body></body></html>"
        mock_get.return_value = mock_response
        
        with pytest.raises(ScraperException) as exc_info:
            scrape_content()
        
        assert "No content found in the page" in str(exc_info.value)
        print("\n✓ Empty response test passed: correctly handled empty HTML")

def test_scrape_content_malformed_html():
    """Test handling of malformed HTML"""
    with patch('scraper.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = "<<<malformed>html>"
        mock_get.return_value = mock_response
        
        with pytest.raises(ScraperException) as exc_info:
            scrape_content()
        
        assert "No content found in the page" in str(exc_info.value)
        print("\n✓ Malformed HTML test passed: correctly handled malformed HTML")

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 