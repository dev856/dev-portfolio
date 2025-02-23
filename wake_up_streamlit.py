#!/usr/bin/env python3
"""
streamlit_wakeup_enhanced.py - Robust Streamlit App Wake-Up System
"""

import os
import time
import random
import requests
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

STREAMLIT_APPS = [
    "https://your-streamlit-app1.streamlit.app/",
    "https://your-streamlit-app2.streamlit.app/",
    "https://your-streamlit-app3.streamlit.app/"
]

def configure_driver():
    """Configure Chrome for reliable CI execution"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--single-process')
    
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def verify_wake_success(driver, url):
    """Multi-stage application status verification"""
    attempts = 0
    while attempts < 6:  # 3-minute total verification window
        try:
            driver.refresh()
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".stApp"))
            )
            
            # Additional API health check
            health_check = requests.get(f"{url}/_stcore/health", timeout=10)
            if health_check.status_code == 200:
                return True
        except (TimeoutException, requests.exceptions.RequestException):
            time.sleep(30)
            attempts += 1
    return False

def maintain_connection(url):
    """Maintain WebSocket connection with randomized intervals"""
    try:
        while True:
            delay = random.randint(25, 35)  # Randomized pattern
            time.sleep(delay)
            requests.post(
                f"{url}/_stcore/stream",
                json={"data": "keepalive"},
                timeout=10
            )
    except KeyboardInterrupt:
        pass

def wake_up_sequence(driver, url, log_file):
    """Full wake-up procedure for a single app"""
    try:
        # Initial wake-up attempt
        driver.get(url)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Handle wake-up button
        try:
            button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Yes, get this app back up!')]")
                )
            )
            button.click()
            log_file.write(f"[{datetime.datetime.now()}] Initiated wake-up for {url}\n")
        except TimeoutException:
            log_file.write(f"[{datetime.datetime.now()}] App already awake: {url}\n")
            return

        # Verification phase
        if verify_wake_success(driver, url):
            log_file.write(f"[{datetime.datetime.now()}] Verified active state: {url}\n")
            # Start keep-alive in background
            import threading
            threading.Thread(target=maintain_connection, args=(url,), daemon=True).start()
        else:
            log_file.write(f"[{datetime.datetime.now()}] Wake-up verification failed: {url}\n")

    except Exception as e:
        log_file.write(f"[{datetime.datetime.now()}] Critical error: {str(e)}\n")

def main():
    driver = configure_driver()
    
    with open("wakeup_log.txt", "a") as log_file:
        log_file.write(f"\n{'='*40}\nSession started: {datetime.datetime.now()}\n{'='*40}\n")
        
        for idx, url in enumerate(STREAMLIT_APPS, 1):
            log_file.write(f"\nProcessing app {idx}/{len(STREAMLIT_APPS)}: {url}\n")
            wake_up_sequence(driver, url, log_file)
    
    driver.quit()

if __name__ == "__main__":
    main()
