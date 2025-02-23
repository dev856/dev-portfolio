# wake_up_apps.py
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Replace with your actual Streamlit apps list or import mechanism
STREAMLIT_APPS = [
    "https://devkotak.streamlit.app/",
    "https://topicapplied.streamlit.app/"
]

def setup_driver():
    """Configure Chrome options for GitHub Actions environment"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def log_message(message, log_file="wakeup_log.txt"):
    """Append timestamped messages to log file"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def wake_apps():
    """Main function to wake up Streamlit apps"""
    driver = setup_driver()
    log_message("=== Starting wake-up sequence ===")
    
    for index, url in enumerate(STREAMLIT_APPS, 1):
        try:
            log_message(f"Processing app {index}/{len(STREAMLIT_APPS)}: {url}")
            driver.get(url)
            
            # Wait for main content to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//main"))
            )
            
            # Attempt to click wake-up button
            try:
                wake_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(., 'Yes, get this app back up!')]")
                    )
                )
                wake_button.click()
                log_message(f"Successfully activated: {url}")
                WebDriverWait(driver, 5).until(EC.staleness_of(wake_button))
            except TimeoutException:
                log_message(f"No activation button found at: {url}")
                
        except Exception as e:
            log_message(f"Error processing {url}: {str(e)}")
            continue
            
    driver.quit()
    log_message("=== Wake-up sequence completed ==="")

if __name__ == "__main__":
    wake_apps()
    sys.exit(0)
