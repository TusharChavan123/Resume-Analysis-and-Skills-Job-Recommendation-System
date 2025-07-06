from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get("http://127.0.0.1:5000")
    return driver

def test_signup_valid():
    driver = setup_driver()
    driver.get("http://127.0.0.1:5000/signup")
    driver.find_element(By.NAME, "username").send_keys("testuser1")
    driver.find_element(By.NAME, "password").send_keys("testpass1")
    driver.find_element(By.NAME, "confirm_password").send_keys("testpass1")
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(1)
    assert "Login" in driver.page_source
    driver.quit()

def test_signup_mismatch_passwords():
    driver = setup_driver()
    driver.get("http://127.0.0.1:5000/signup")
    driver.find_element(By.NAME, "username").send_keys("testuser2")
    driver.find_element(By.NAME, "password").send_keys("testpass1")
    driver.find_element(By.NAME, "confirm_password").send_keys("wrongpass")
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(1)
    assert "Passwords do not match" in driver.page_source
    driver.quit()

def test_signup_existing_user():
    driver = setup_driver()
    driver.get("http://127.0.0.1:5000/signup")
    driver.find_element(By.NAME, "username").send_keys("testuser1")
    driver.find_element(By.NAME, "password").send_keys("testpass1")
    driver.find_element(By.NAME, "confirm_password").send_keys("testpass1")
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(1)
    assert "Username already exists" in driver.page_source
    driver.quit()

def test_login_valid():
    driver = setup_driver()
    driver.get("http://127.0.0.1:5000/login")
    driver.find_element(By.NAME, "username").send_keys("testuser1")
    driver.find_element(By.NAME, "password").send_keys("testpass1")
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(1)
    assert "Logout" in driver.page_source or "Welcome" in driver.page_source
    driver.quit()

def test_login_invalid():
    driver = setup_driver()
    driver.get("http://127.0.0.1:5000/login")
    driver.find_element(By.NAME, "username").send_keys("invaliduser")
    driver.find_element(By.NAME, "password").send_keys("wrongpass")
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(1)
    assert "Invalid username or password" in driver.page_source
    driver.quit()



# Optional runner
if __name__ == "__main__":
    test_signup_valid()
    test_signup_mismatch_passwords()
    test_signup_existing_user()
    test_login_valid()
    test_login_invalid()
    print("✅ All tests completed.")

