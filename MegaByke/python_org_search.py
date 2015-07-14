from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()


driver.get("http://104.236.97.57:8888/RoutePlanner/")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source

#submit = driver.find_element_by_name("update")
#submit.click()


driver.close()