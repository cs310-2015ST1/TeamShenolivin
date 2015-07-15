__author__ = 'Sharon'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Firefox()

driver.get("http://104.236.97.57:8888/RoutePlanner/")
assert "Route" in driver.title
assert "No results found." not in driver.page_source

location1 = driver.find_element_by_id("locationInput1")
location2 = driver.find_element_by_id("locationInput2")
spinner1 = driver.find_element_by_id("spinner1")
spinner2 = driver.find_element_by_id("spinner2")
plotRoute = driver.find_element_by_css_selector("Plot Routes")
plotAllRoutes = driver.find_element_by_css_selector("Plot All Routes")

#type invalid location then clear

enter1 = ActionChains(driver)
enter1.move_to_element(location1)
enter1.send_keys("harbour")
enter1.send_keys(Keys.ARROW_DOWN)
enter1.send_keys(Keys.ENTER)
enter1.perform()
alert = driver.switch_to.alert.accept()

enter2 = ActionChains(driver)
enter2.move_to_element(location2)
enter2.send_keys("oakridge")
enter2.send_keys(Keys.ARROW_DOWN)
enter2.send_keys(Keys.ENTER)
enter2.perform()
alert = driver.switch_to.alert.accept()

spinner1.send_keys("1")
spinner2.send_keys("2")

plotRoute.click()

driver.refresh()

driver.close()
