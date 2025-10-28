#!/usr/bin/env python3
"""
Web Scraper - Flexible Web Data Extraction Tool

This script provides a flexible framework for extracting data from websites.
It uses BeautifulSoup for HTML parsing and supports various output formats
including JSON, CSV, and plain text.

Usage:
    python web_scraper.py <url> [options]
    
Example:
    python web_scraper.py https://example.com --output data.json

Features:
    - Parse HTML content from any URL
    - Extract specific elements using CSS selectors
    - Support for multiple output formats
    - Error handling and retry logic

Author: automation-scripts
License: MIT
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import sys
import time
from urllib.parse import urljoin, urlparse

class WebScraper:
    """A flexible web scraper for extracting data from websites."""
    
    def __init__(self, url, timeout=10, max_retries=3):
        """
        Initialize the web scraper.
        
        Args:
            url (str): The URL to scrape
            timeout (int): Request timeout in seconds
            max_retries (int): Maximum number of retry attempts
        """
        self.url = url
        self.timeout = timeout
        self.max_retries = max_retries
        self.soup = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def fetch_page(self):
        """Fetch the webpage content with retry logic."""
        for attempt in range(self.max_retries):
            try:
                print(f"Fetching {self.url}... (Attempt {attempt + 1}/{self.max_retries})")
                response = requests.get(
                    self.url,
                    headers=self.headers,
                    timeout=self.timeout
                )
                response.raise_for_status()
                self.soup = BeautifulSoup(response.content, 'html.parser')
                print("Page fetched successfully!")
                return True
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    print("Max retries reached. Failed to fetch page.")
                    return False
    
    def extract_links(self):
        """Extract all links from the page."""
        if not self.soup:
            print("Error: Page not loaded. Call fetch_page() first.")
            return []
        
        links = []
        for link in self.soup.find_all('a', href=True):
            absolute_url = urljoin(self.url, link['href'])
            links.append({
                'text': link.get_text(strip=True),
                'url': absolute_url
            })
        return links
    
    def extract_text(self, selector=None):
        """Extract text content from the page or specific elements."""
        if not self.soup:
            print("Error: Page not loaded. Call fetch_page() first.")
            return ""
        
        if selector:
            elements = self.soup.select(selector)
            return [elem.get_text(strip=True) for elem in elements]
        else:
            return self.soup.get_text(strip=True)
    
    def extract_images(self):
        """Extract all image URLs from the page."""
        if not self.soup:
            print("Error: Page not loaded. Call fetch_page() first.")
            return []
        
        images = []
        for img in self.soup.find_all('img', src=True):
            absolute_url = urljoin(self.url, img['src'])
            images.append({
                'alt': img.get('alt', ''),
                'url': absolute_url
            })
        return images
    
    def save_to_json(self, data, filename):
        """Save extracted data to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Data saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving to JSON: {e}")
            return False
    
    def save_to_csv(self, data, filename):
        """Save extracted data to a CSV file."""
        try:
            if not data:
                print("No data to save.")
                return False
            
            keys = data[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            print(f"Data saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            return False

def main():
    """
    Main function demonstrating basic web scraping usage.
    Customize this function based on your specific scraping needs.
    """
    if len(sys.argv) < 2:
        print("Usage: python web_scraper.py <url> [output_file]")
        print("Example: python web_scraper.py https://example.com data.json")
        return
    
    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'scraped_data.json'
    
    # Create scraper instance
    scraper = WebScraper(url)
    
    # Fetch the page
    if not scraper.fetch_page():
        print("Failed to fetch the page. Exiting.")
        return
    
    # Extract data
    print("\nExtracting data...")
    links = scraper.extract_links()
    images = scraper.extract_images()
    
    # Prepare data for export
    data = {
        'url': url,
        'total_links': len(links),
        'total_images': len(images),
        'links': links[:10],  # First 10 links
        'images': images[:10]  # First 10 images
    }
    
    # Save to file
    scraper.save_to_json(data, output_file)
    print(f"\nScraping complete! Found {len(links)} links and {len(images)} images.")

if __name__ == "__main__":
    main()
