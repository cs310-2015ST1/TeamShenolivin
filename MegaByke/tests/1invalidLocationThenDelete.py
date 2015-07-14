from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()


driver.get("http://104.236.97.57:8888/RoutePlanner/")
assert "Route" in driver.title
assert "No results found." not in driver.page_source

location1 = driver.find_element_by_id("locationInput1")
location2 = driver.find_element_by_id("locationInput2")

#click about
#about = driver.find_element_by_partial_link_text("About")
#about.click()


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





#driver.close()
