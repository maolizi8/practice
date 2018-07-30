from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


class Base(object):
    def __init__(self, driver):
        self.driver = driver
    
    # 重新封装单个元素定位方法
    def find_element(self, loc):
        """
        单个元素定位方法
        @param loc: 元素定位 ，例如：(By.ID, "kw")
        @return: 单个元素
        """
        msg="未能找到元素: %s " % (loc,)
        try:
            #WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element(*loc).is_displayed())
            WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(loc),message=msg)
            return self.driver.find_element(*loc)
        except Exception:
            print(msg)
            raise Exception(msg)

    # 重新封装一组元素定位方法
    def find_elements(self, loc):
        """
        一组元素定位方法
        @param loc: 元素定位 ，例如：(By.ID, "kw")
        @return: 元素列表/空列表
        """
        
        try:
            msg="未能找到元素: %s " % (loc,)
            WebDriverWait(self.driver, 15).until(EC.visibility_of_any_elements_located(loc),message=msg)
            return self.driver.find_elements(*loc)
        except Exception:
            print(msg)
            return []

    
    def switch_to_latest_windows(self):
        """
        浏览器多窗口，切换到最新窗口
        @return: 
        """
        handles = self.driver.window_handles  # 获取所有窗口句柄
        self.driver.switch_to_window(handles[-1])  # 切换到最新窗口
        return self.driver.current_window_handle

    def get_last_window_title(self):
        """
        浏览器多窗口，获取最新窗口标题
        @return: 
        """
        handles = self.driver.window_handles  # 获取所有窗口句柄
        current_handle = self.driver.current_window_handle  # 保存当前窗口句柄
        self.driver.switch_to_window(handles[-1])  # 切换到弹出窗口
        title = self.driver.title  # 获取标题
        self.driver.switch_to_window(current_handle)  # 切换回原窗口
        return title

    def close_latest_window(self):
        """
        浏览器多窗口，关闭最后一个窗口
        @return: 
        """
        handles = self.driver.window_handles  # 获取所有窗口句柄
        self.driver.switch_to_window(handles[-1])  # 切换到弹出窗口
        self.driver.close()  # 关闭
        self.driver.switch_to_window(handles[-2])  # 切换回上一个窗口

