from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def visit_user_page(url, adminpwd):
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
         command_executor="http://selenium-hub:4444",
         options=options
    )
    try:
        print(f"Visiting {url}")
        driver.implicitly_wait(5)  # 5 sec timeout for finding elements
        driver.get("http://secretdiary:8080/login")
        login_f = driver.find_element(By.ID, "usernameinput")
        login_f.send_keys("santaclaus")
        pw_f = driver.find_element(By.ID, "passwordinput")
        pw_f.send_keys(adminpwd)
        pw_f.send_keys(Keys.ENTER)
        driver.get(url)
        sleep(5)  # Carefully read the diary of the user for five seconds
    finally:
        driver.quit()

