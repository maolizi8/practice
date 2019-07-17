'''
Created on 2017年7月29日

@author: gql
'''
from time import sleep
from business import Resources as R
from business import BasePage 

class Homepage(BasePage.Base):
    HOME_URL="http://www.baidu.com"
    
    def open_baidu(self):
        self.driver.get(self.HOME_URL)
        sleep(2)
        print(self.driver.title)     
        
    def baidu_search(self,keyword):
        search_input=self.find_element(R.Home.search_input)
        search_input.clear()
        search_input.send_keys(keyword)
        print('搜索关键词： ',keyword)
        self.find_element(R.Home.search_button).click()
        sleep(2)
        print(self.driver.title)
        return self.driver.title

if __name__=="__main__":
    pass