__author__ = 'Sharon'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

driver.get("http://104.236.97.57:8888/RoutePlanner/register.html")
assert "Route" in driver.title
assert "No results found." not in driver.page_source

username = driver.find_element_by_id("id_username")
email = driver.find_element_by_id("id_email")
password = driver.find_element_by_id("id_password")
register = driver.find_element_by_name("submit")

#this should be unsuccessful, existing account
username.send_keys("Admin")
password.send_keys("Admin")
register.click()

driver.find_element_by_id("id_username").clear()

driver.refresh()
alert = driver.switch_to.alert.accept()

#this should fail, invalid characters
#username.send_keys("abc$$")
#password.send_keys("asdf")
#register.click()

#this should work
#username.send_keys("qwerty")
#email.send_keys("qwerty@gmail.com")
#password.send_keys("qwerty")

driver.close()