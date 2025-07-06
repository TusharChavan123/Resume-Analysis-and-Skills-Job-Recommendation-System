import os
import time
import requests
import random
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

def test_register():
    """Tests the registration functionality."""
    driver.get(f"{BASE_URL}/signup")

    print("Before Register - Page Title:", driver.title)
    print("Before Register - Current URL:", driver.current_url)

    # Generate a unique test user
    unique_username = f"testuser{random.randint(1000, 9999)}"
    password = "Test@1234"

    # Locate form fields
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    confirm_password_field = driver.find_element(By.NAME, "confirm_password")

    # Fill in the form
    username_field.send_keys(unique_username)
    password_field.send_keys(password)
    confirm_password_field.send_keys(password)

    # Submit the form
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    # Wait for potential redirect or error display
    time.sleep(2)
    print("After Register - Page Title:", driver.title)
    print("After Register - Current URL:", driver.current_url)

    # Determine if registration was successful
    if driver.current_url != f"{BASE_URL}/signup":
        print("✅ Registration successful! Redirected to login or dashboard.")
    else:
        try:
            error_message = driver.find_element(By.CLASS_NAME, "error").text
            print("❌ Registration failed with error:", error_message)
        except:
            print("❌ Registration failed for unknown reason.")
        raise AssertionError("Registration failed!")

def run_tests():
    print("🚀 Running Selenium registration test...")

    wait_for_server()  # Ensure Flask is running before proceeding

    try:
        test_register()
        print("✅ All tests passed!")
    except AssertionError as e:
        print("❌ Test failed:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_tests()
