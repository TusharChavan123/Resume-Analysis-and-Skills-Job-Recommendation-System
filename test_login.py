import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Flask app URL
BASE_URL = "http://127.0.0.1:5000"


# Initialize WebDriver using WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def wait_for_server():
    """Waits until the Flask server is running."""
    print("⏳ Checking if Flask server is running...")
    while True:
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                print("✅ Flask server is up and running!")
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(2)

def test_login():
    """Tests the login functionality."""
    driver.get(f"{BASE_URL}/login")
    
    print("Before Login - Page Title:", driver.title)
    print("Before Login - Current URL:", driver.current_url)

    # Locate username and password fields
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    # Enter credentials (Use environment variables for security)
    username_field.send_keys(os.getenv("TEST_USERNAME", "tusharchavan"))
    password_field.send_keys(os.getenv("TEST_PASSWORD", "tushar123"))

    # Click the login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    # Wait for dashboard redirection
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    except:
        print("❌ Login failed! Page did not redirect in time.")
        return  

    print("After Login - Page Title:", driver.title)
    print("After Login - Current URL:", driver.current_url)
    assert "AI-Powered Resume Ranking System" in driver.title or driver.current_url == f"{BASE_URL}/", "Login failed!"

    
def run_tests():
    print("🚀 Running Selenium tests...")
    
    wait_for_server()  # Ensure Flask is running before proceeding
    
    try:
        test_login()
        print("✅ All tests passed!")
    except AssertionError as e:
        print("❌ Test failed:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_tests()
