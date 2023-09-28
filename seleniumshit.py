import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
driver = webdriver.Firefox()

driver.get("https://www.instagram.com/accounts/login")
time.sleep(5)
username = driver.find_element('name','username')
username.send_keys("ori.gami0425")
print("Typing username")
time.sleep(5)
password = driver.find_element('name','password')
password.send_keys("SHANGNANpranav+244872")
print("Typing Password")
time.sleep(5)
loginbut = driver.find_element(By.XPATH, '//button[@type="submit"]')
loginbut.click()