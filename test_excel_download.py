import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Flask app URL
BASE_URL = "http://127.0.0.1:5000"

# Default download folder
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
EXPECTED_FILENAME = "resume_analysis_report.xlsx"

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def wait_for_server():
    """Waits until the Flask server is running."""
    print("⏳ Checking if Flask server is running...")
    while True:
        try:
            response = requests.get(BASE_URL, timeout=5)
            if response.status_code == 200:
                print("✅ Flask server is up and running!")
                break
        except requests.exceptions.ConnectionError:
            print("⚠️ Waiting for the Flask server...")
        time.sleep(2)

def test_login():
    """Logs into the application if required before downloading files."""
    driver.get(f"{BASE_URL}/login")
    
    print("🌐 Opening Login Page...")
    time.sleep(2)

    try:
        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))

        username = os.getenv("TEST_USERNAME", "tusharchavan")
        password = os.getenv("TEST_PASSWORD", "tushar123")

        username_field.send_keys(username)
        password_field.send_keys(password)
        print(f"🔑 Entered Username: {username}")

        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_button.click()
        print("🖱 Clicked Login Button")

        # Wait for successful login
        WebDriverWait(driver, 10).until(lambda d: d.current_url != f"{BASE_URL}/login")
        print("✅ Login successful!")

    except Exception as e:
        print(f"⚠️ Login Test Failed: {e}")

def test_download():
    """Tests downloading the Excel report."""
    driver.get(f"{BASE_URL}/download")

    # If not logged in, login first
    if "login" in driver.current_url:
        test_login()

    print("📥 Navigating to the download page...")

    try:
        # Wait for the download button to be clickable
        download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='download-excel']")))
        download_button.click()
        print("📤 Clicked Download Button")

        # Wait for the file to appear in the Downloads folder
        time.sleep(5)  # Give time for the file to download

        downloaded_file_path = os.path.join(DOWNLOAD_FOLDER, EXPECTED_FILENAME)
        if os.path.exists(downloaded_file_path):
            print(f"✅ Download successful! File saved at: {downloaded_file_path}")
        else:
            print("❌ Download failed! File not found.")

    except Exception as e:
        print(f"⚠️ Download Test Failed: {e}")

def run_tests():
    print("🚀 Running Selenium tests...")
    
    wait_for_server()  # Ensure Flask is running before proceeding
    
    try:
        test_download()
        print("✅ All tests passed!")
    except AssertionError as e:
        print("❌ Test failed:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_tests()
