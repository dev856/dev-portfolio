#!/usr/bin/env python3
"""
streamlit_wakeup_enhanced.py - Robust Streamlit Wake-Up System
"""

import os
import time
import random
import requests
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    filename='wakeup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

STREAMLIT_APPS = [
    "https://devkotak.streamlit.app",
    "https://topicapplied.streamlit.app"
]

CHROME_OPTIONS = [
    '--headless=new',
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-software-rasterizer',
    '--window-size=1920,1080',
    '--single-process',
    '--remote-allow-origins=*'
]

def create_driver():
    """Create a fresh browser instance with stability enhancements"""
    options = webdriver.ChromeOptions()
    for option in CHROME_OPTIONS:
        options.add_argument(option)
    
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def validate_session(driver):
    """Check if the current browser session is still valid"""
    try:
        driver.title
        return True
    except WebDriverException:
        return False

def wake_app(url):
    """Execute full wake-up sequence with error recovery"""
    driver = None
    try:
        driver = create_driver()
        
        # Phase 1: Initial page load
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Phase 2: Button interaction
        try:
            button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Yes, get this app back up!')]")
                )
            )
            button.click()
            logging.info(f"Wake-up triggered for {url}")
        except Exception as e:
            logging.warning(f"No button found for {url}: {str(e)}")
            return

        # Phase 3: Post-wake verification
        verification_passed = False
        for attempt in range(3):
            try:
                driver.refresh()
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".stApp"))
                )
                verification_passed = True
                break
            except Exception as e:
                logging.warning(f"Verification attempt {attempt+1} failed: {str(e)}")
                time.sleep(10)
        
        if verification_passed:
            logging.info(f"Successfully woke {url}")
        else:
            logging.error(f"Failed to verify wake-up for {url}")

    except Exception as e:
        logging.error(f"Critical error processing {url}: {str(e)}")
    finally:
        if driver and validate_session(driver):
            driver.quit()

def main():
    """Main execution flow with session management"""
    for index, url in enumerate(STREAMLIT_APPS, 1):
        logging.info(f"Processing app {index}/{len(STREAMLIT_APPS)}: {url}")
        wake_app(url)
        time.sleep(random.uniform(1, 3))  # Add jitter between requests

if __name__ == "__main__":
    main()
