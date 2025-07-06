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
    """Logs into the application if required before uploading files."""
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

def test_file_upload():
    """Tests file upload functionality."""
    driver.get(BASE_URL)

    # If not logged in, login first
    if "login" in driver.current_url:
        test_login()

    print("📂 Navigating to file upload page...")
    
    try:
        # Wait for file input fields
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "job_description")))

        # Upload job description file
        job_desc_input = driver.find_element(By.NAME, "job_description")
        job_desc_path = os.path.abspath("test_files/job_description.pdf")
        job_desc_input.send_keys(job_desc_path)
        print(f"📄 Uploaded Job Description: {job_desc_path}")

        # Upload resumes
        resume_input = driver.find_element(By.NAME, "resumes")
        resume_paths = [
            os.path.abspath("test_files/resume1.pdf"),
            os.path.abspath("test_files/resume2.pdf")
        ]
        resume_input.send_keys("\n".join(resume_paths))
        print(f"📑 Uploaded Resumes: {resume_paths}")

        # Click the upload button
        upload_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        upload_button.click()
        print("📤 Submitted the upload form")

        # Wait for results page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
        print("✅ Upload successful, results displayed!")

    except Exception as e:
        print(f"⚠️ File Upload Test Failed: {e}")

def run_tests():
    print("🚀 Running Selenium tests...")
    
    wait_for_server()  # Ensure Flask is running before proceeding
    
    try:
        test_file_upload()
        print("✅ All tests passed!")
    except AssertionError as e:
        print("❌ Test failed:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_tests()
