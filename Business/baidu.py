from selenium import webdriver
from time import sleep



def bd_search(driver,url):
    driver.get(url)
    sleep(2)
    search_in=driver.find_element_by_id('kw')
    search_in.clear()
    search_in.send_keys('python')
    driver.find_element_by_id('su').click()
    sleep(2)
    print(driver.title)

if __name__=="__main__":
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    url='https://www.baidu.com/'
    bd_search(driver,url)