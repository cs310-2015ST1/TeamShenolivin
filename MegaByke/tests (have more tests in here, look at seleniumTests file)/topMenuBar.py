__author__ = 'Sharon'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

driver.get("http://104.236.97.57:8000/RoutePlanner/")
assert "Route" in driver.title
assert "No results found." not in driver.page_source

#click about
about = driver.find_element_by_link_text("About")
driver.click(about)

#driver.close()