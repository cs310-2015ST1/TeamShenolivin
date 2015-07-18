__author__ = 'Sharon'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://104.236.97.57:8000/RoutePlanner/")
assert "Route" in driver.title
assert "No results found." not in driver.page_source

location1 = driver.find_element_by_id("locationInput1")
location2 = driver.find_element_by_id("locationInput2")

#type invalid location then clear
location1.send_keys("harbour")
delete1 = driver.find_element_by_xpath("//img[contains(@src, 'redX.png')]/..")
delete1.click()
alert = driver.switch_to.alert.accept()

#type invalid location then try to type in next box
location1.send_keys("harbour")
try:
    location2.send_keys("harbour")
    print "shouldn't have been allowed"
except:
    print "this should happen"

#login as Admin
driver.get("http://104.236.97.57:8000/RoutePlanner/login.html")
assert "Route" in driver.title
assert "No results found." not in driver.page_source

username = driver.find_element_by_name("username")
password = driver.find_element_by_name("password")

username.send_keys("Admin")
password.send_keys("Admin")
password.send_keys(Keys.ENTER)

#log in with invalid account
driver.get("http://104.236.97.57:8000/RoutePlanner/login.html")
assert "Route" in driver.title
assert "No results found." not in driver.page_source

username = driver.find_element_by_name("username")
password = driver.find_element_by_name("password")

username.send_keys("###")
password.send_keys("asdf")
password.send_keys(Keys.ENTER)
assert "login details" in driver.page_source

#log in with valid account
driver.get("http://104.236.97.57:8000/RoutePlanner/login.html")
assert "Route" in driver.title
assert "No results found." not in driver.page_source

username = driver.find_element_by_name("username")
password = driver.find_element_by_name("password")

username.send_keys("sharon")
password.send_keys("yang")
password.send_keys(Keys.ENTER)
assert "sharon" in driver.page_source

#now test account creation
driver.get("http://104.236.97.57:8000/RoutePlanner/register.html")
assert "Route" in driver.title
assert "No results found." not in driver.page_source

username = driver.find_element_by_id("id_username")
email = driver.find_element_by_id("id_email")
password = driver.find_element_by_id("id_password")

#this should be unsuccessful, existing account
username.send_keys("Admin")
password.send_keys("Admin")
password.send_keys(Keys.ENTER)

#unsuccessful because invalid characters
driver.get("http://104.236.97.57:8000/RoutePlanner/register.html")
assert "Route" in driver.title
assert "No results found." not in driver.page_source

username = driver.find_element_by_id("id_username")
email = driver.find_element_by_id("id_email")
password = driver.find_element_by_id("id_password")

username.send_keys("###")
email.send_keys("abc@abc.com")
password.send_keys("Admin")
password.send_keys(Keys.ENTER)

#have to test making valid account by hand because script can only be run once

#test plotting
driver.get("http://104.236.97.57:8000/RoutePlanner/")
assert "Route" in driver.title
assert "No results found." not in driver.page_source

location1 = driver.find_element_by_id("locationInput1")
location2 = driver.find_element_by_id("locationInput2")
spinner1 = driver.find_element_by_id("spinner1")
spinner2 = driver.find_element_by_id("spinner2")

#plot and save a point
location1.send_keys("vandusen")
location1.click()
location1.send_keys(Keys.ARROW_DOWN)
location1.send_keys(Keys.ENTER)


driver.close()