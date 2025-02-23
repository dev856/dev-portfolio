#!/usr/bin/env python3
"""
streamlit_wakeup.py

Automatically wakes up Streamlit apps deployed on free hosting platforms.
Configured for GitHub Actions with headless Chrome and automatic driver management.
"""

import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# List of Streamlit app URLs to wake up (replace with your actual apps)
STREAMLIT_APPS = [
    "https://devkotak.streamlit.app/",
    "https:///topicapplied.streamlit.app/"
]

def wake_up_apps():
    """Main function to wake up all specified Streamlit apps"""
    # Configure Chrome options for headless execution in CI
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    # Set up ChromeDriver with automatic version management
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Execute wake-up sequence for each app
    with open("wakeup_log.txt", "a") as log_file:
        log_file.write(f"\n{'='*40}\nExecution started: {datetime.datetime.now()}\n{'='*40}\n")
        
        for index, url in enumerate(STREAMLIT_APPS, 1):
            try:
                log_file.write(f"\n[{index}/{len(STREAMLIT_APPS)}] Processing: {url}\n")
                driver.get(url)
                
                # Wait for page to load
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                # Attempt to click wake-up button
                try:
                    button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//button[contains(., 'Yes, get this app back up!')]")
                        )
                    )
                    button.click()
                    log_file.write(f"[SUCCESS] App awakened\n")
                except TimeoutException:
                    log_file.write(f"[INFO] App already awake\n")

            except Exception as e:
                log_file.write(f"[ERROR] {str(e)}\n")

    # Clean up resources
    driver.quit()

if __name__ == "__main__":
    wake_up_apps()
