__author__ = 'Sharon'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

driver.get("http://104.236.97.57:8000/RoutePlanner/register.html")
assert "Route" in driver.title
assert "No results found." not in driver.page_source

username = driver.find_element_by_id("id_username")
email = driver.find_element_by_id("id_email")
password = driver.find_element_by_id("id_password")
register = driver.find_element_by_name("submit")

#this should work only once, then will become a duplicated account
username.send_keys("qwerty")
email.send_keys("qwerty@gmail.com")
password.send_keys("qwerty")
register.click()

#driver.close()