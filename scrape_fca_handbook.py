#!/usr/bin/env python3
"""
Script to scrape FCA Handbook CASS pages and save as text files.
Uses Selenium to handle JavaScript-rendered content.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os

def setup_driver():
    """Set up Chrome driver with headless options."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error setting up Chrome driver: {e}")
        print("Trying to use Safari driver instead...")
        try:
            driver = webdriver.Safari()
            return driver
        except Exception as e2:
            print(f"Error setting up Safari driver: {e2}")
            return None

def scrape_fca_handbook(driver, page_id):
    """
    Scrape a single FCA handbook CASS page.

    Args:
        driver: Selenium WebDriver instance
        page_id: The CASS page identifier (e.g., '1', '7a', 'tp1', 'sch1')

    Returns:
        str: The extracted text content
    """
    url = f"https://handbook.fca.org.uk/handbook/cass{page_id}"

    try:
        print(f"Fetching CASS{page_id}...")
        driver.get(url)

        # Wait for content to load (wait for body to be present and JavaScript to execute)
        time.sleep(5)  # Give JavaScript time to execute

        # Get page text
        text = driver.find_element(By.TAG_NAME, 'body').text

        return text

    except Exception as e:
        print(f"Error fetching CASS{page_id}: {e}")
        return None

def main():
    """Main function to scrape all CASS pages."""

    # Create output directory
    output_dir = "fca_handbook_cass"
    os.makedirs(output_dir, exist_ok=True)

    # Define all page IDs to scrape
    page_ids = (
        # Numbered pages 1-14
        [str(i) for i in range(1, 15)] +
        # Additional pages with suffixes
        ['1a', '7a', 'tp1', 'sch1', 'sch2', 'sch3', 'sch4', 'sch5', 'sch6']
    )

    # Set up driver
    driver = setup_driver()
    if not driver:
        print("Failed to initialize web driver. Please install Chrome or ensure Safari driver is enabled.")
        return

    try:
        success_count = 0
        fail_count = 0

        for page_id in page_ids:
            content = scrape_fca_handbook(driver, page_id)

            if content and len(content) > 200:  # Check if we got meaningful content
                output_file = os.path.join(output_dir, f"cass{page_id}.txt")
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ Saved to {output_file} ({len(content)} bytes)")
                success_count += 1
            else:
                print(f"✗ Failed to scrape CASS{page_id} or content too short")
                fail_count += 1

            # Be polite - add a small delay between requests
            time.sleep(2)

        print(f"\nCompleted: {success_count} successful, {fail_count} failed")
        print(f"Files saved in: {os.path.abspath(output_dir)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
