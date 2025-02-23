from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from streamlit_app import STREAMLIT_APPS
import datetime
import time

# Set up Selenium webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Initialize log file
with open("wakeup_log.txt", "a") as log_file:
    log_file.write(f"Execution started at: {datetime.datetime.now()}\n")

    # Iterate through each URL in the list
    for url in STREAMLIT_APPS:
        try:
            # Navigate to the webpage
            driver.get(url)
            
            # Wait for the page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Check if the wake up button exists
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Yes, get this app back up!']"))
                )
                button.click()

                # Wait for the button to disappear, indicating the app is waking up
                WebDriverWait(driver, 120).until_not(
                    EC.presence_of_element_located((By.XPATH, "//button[text()='Yes, get this app back up!']"))
                )

                # Optionally, get the page title to confirm it's awake
                title = driver.title
                log_file.write(f"[{datetime.datetime.now()}] Successfully woke up app at: {url}. Title: {title}\n")
            except TimeoutException as e:
                log_file.write(f"[{datetime.datetime.now()}] Button not found or did not disappear for app at: {url}\n")
        
        except Exception as e:
            log_file.write(f"[{datetime.datetime.now()}] Error for app at {url}: {str(e)}\n")

        # Wait for 10 seconds before moving to the next app
        time.sleep(10)

# Close the browser
driver.quit()
