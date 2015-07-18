from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Firefox()

driver.get("http://104.236.97.57:8000/RoutePlanner/")
assert "Route" in driver.title
assert "No results found." not in driver.page_source

location1 = driver.find_element_by_id("locationInput1")
location2 = driver.find_element_by_id("locationInput2")
spinner1 = driver.find_element_by_id("spinner1")
spinner2 = driver.find_element_by_id("spinner2")


#type invalid location then clear

location1.send_keys("vandusen")
location1.click()
location1.send_keys(Keys.ARROW_DOWN)
location1.send_keys(Keys.ENTER)
driver.refresh()
location2.send_keys("oakridge")
location2.click()
location2.send_keys(Keys.ARROW_DOWN)
location2.send_keys(Keys.ENTER)

driver.close()
