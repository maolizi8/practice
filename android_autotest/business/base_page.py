'''
Created on 2018年8月8日

@author: geqiuli
'''
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from component.Resources import Public as P
from time import sleep
import subprocess
import time,os

class Base:
    '''driver的一些基础封装'''
    
    def __init__(self,driver):
        self.driver=driver
        
    def wait_until_display(self,element,message='查找元素失败',timeout=30):
        '''等待元素显示
        @param element: 元素定位方法，类似： (By.ID, "abc")
        '''
        WebDriverWait(self.driver,timeout).until(EC.visibility_of_element_located(element[:2]),message=message)
                
    def find_element(self, loc, ele_desc=None):
        '''查找元素
        @param loc: 元素定位方法，类似： (By.ID, "abc")
        @param ele_desc: 元素描述
        @return: 单个元素
        '''
        try:
            self.wait_until_display(loc[:2])
            ele=self.driver.find_element(*loc[:2])
            return ele
        except TimeoutException:
            if ele_desc:
                msg='查找元素超时：'+ele_desc
            else:
                msg='查找元素超时：'+str(loc)
            print(msg)
            raise Exception(msg)
        except Exception:
            if ele_desc:
                msg='查找元素异常：'+ele_desc
            else:
                msg='查找元素异常：'+str(loc)
            print(msg)
            raise Exception(msg)
    
    def find_elements(self, loc, ele_desc=None):
        '''查找元素
        @param loc: 元素定位方法，类似： (By.ID, "abc")
        @param ele_desc: 元素描述
        @return: 元素列表
        '''
        try:
            WebDriverWait(self.driver,15).until(EC.visibility_of_any_elements_located(loc[:2]),message='timeout')

            ele=self.driver.find_elements(*loc[:2])
            return ele
        except TimeoutException:
            return []
        except Exception:
            if ele_desc:
                msg='查找元素超时：'+ele_desc
            else:
                msg='查找元素超时：'+str(loc)
            print(msg)
            return []           
    
    
    def find_child_use_loc(self, father_loc, children_loc, ele_desc=None):
        '''查找后代元素
        @param father_loc: 父元素定位方法，类似： (By.ID, "abc")
        @param children_loc: 后代元素定位方法，类似： (By.ID, "abc")'''
        try:
            WebDriverWait(self.driver,30).until(EC.visibility_of_any_elements_located(father_loc[:2]),message='timeout')
            father_ele=self.driver.find_element(*father_loc[:2])
            child_ele=father_ele.find_element(*children_loc[:2])
            return child_ele
        except Exception:
            if ele_desc:
                msg='查找元素超时：'+ele_desc
                print(msg)
            raise Exception(msg)  
    
    def find_child_use_ele(self, father_ele, children_loc, ele_desc=None):
        '''查找后代元素
        @param father_ele: 已定位的父元素
        @param children_loc: 后代元素定位方法，类似： (By.ID, "abc")'''
        try:
            child_ele=father_ele.find_element(*children_loc[:2])
            return child_ele
        except Exception:
            if ele_desc:
                msg='查找元素超时：'+ele_desc
                print(msg)
            raise Exception(msg)  
            
    def return_by_head(self, target=None):
        '''页头-返回按钮
        @param target: 返回到目标activity，例如返回：.HomeActivity'''
        print(self.driver.current_context)
        try:
            self.wait_until_display(P.top_title_close, timeout=5)
            self.find_element(P.top_title_close, '顶部关闭按钮').click()
            sleep(1)
        except Exception:
            self.find_element(P.top_title_back, '顶部返回按钮').click()
            sleep(1)
        if target:
            self.driver.wait_activity(target,3)    
#         if self.driver.current_context=='NATIVE_APP':
#              
#         else:
#             pass
        
    def return_by_device(self, target=None):
        '''手机物理键-返回
        @param target: 返回到目标activity，例如返回：.HomeActivity'''
        
        if target:
            if target!=self.driver.current_activity:
                self.driver.press_keycode(4)
            self.driver.wait_activity(target,3)
        else:
            print("物理键返回")
            self.driver.press_keycode(4)
        sleep(0.5)
      
    
    def switch_to_webview(self, webview,message=None):
        if webview not in self.driver.contexts:
            if message:
                raise Exception(message)
            else:
                print('当前view: ',self.driver.contexts)
                raise Exception('未找到H5页面：',webview)
        self.driver.switch_to.context(webview)
    
    def switch_to_native_app(self):
        if self.driver.current_context!='NATIVE_APP':
            self.driver.switch_to.context('NATIVE_APP')
        
    def swipe_to_bottom(self):
        ''''''
        body = self.find_element(P.body_content)
        x1=body.location.get('x')
        y1=body.location.get('y')
        height=body.size.get("height")
        width=body.size.get("width")
        while True:
            previous_page=self.driver.page_source
            self.driver.swipe(x1+width/2,y1+height/2,x1+width/2,y1)
            current_page=self.driver.page_source
            if current_page==previous_page:
                break
            sleep(1)
            
    def swipe_to_element(self,ele_loc,message='查找元素失败'):
        '''
        @param  ele_code: 用于识别元素的代码，例如：resource-id="com.app:id/upload_submit_btn"
        @param ele_loc: 用于定位元素的方法，例如：(By.ID, "com.app:id/upload_submit_btn")
        '''
        content = self.find_element(P.body_content)
        x1=content.location.get('x')
        y1=content.location.get('y')
        height=content.size.get("height")
        width=content.size.get("width")
#         print(self.driver.page_source)
        while True:
            previous_page=self.driver.page_source
            try:
                self.wait_until_display(ele_loc,message=message, timeout=2)
            except Exception:
                self.driver.swipe(x1+width/2,y1+height/2,x1+width/2,y1)
                current_page=self.driver.page_source
                if current_page==previous_page:
                    raise Exception(message)
            else:
                break
    def swip_to_direction(self,ele_loc, turn='left', message='查找元素失败'):
        '''某个元素位置向左滑动'''
        content = self.find_element(ele_loc)
        x1=content.location.get('x')
        y1=content.location.get('y')
        height=content.size.get("height")
        width=content.size.get("width")
        print("位置：",x1,y1,height,width)
        previous_page=self.driver.page_source
        if turn =='left':
            self.driver.swipe(x1+width*0.99,y1,x1,y1)
            current_page=self.driver.page_source
            if current_page==previous_page:
                    raise Exception(message)
        elif turn == "up":
            print("向上滑动")
            self.driver.swipe(x1,y1+width*0.7,x1,y1)
    
    
    
    def wait_activity(self,activity,timeout=10):
        self.driver.wait_activity(activity,timeout)
        
    def close_chromedriver(self): 
        '''关闭chromedriver'''
        subprocess.Popen('taskkill /F /im chromedriver.exe', shell=True, stdout=subprocess.PIPE)
        sleep(5)
   

    def swipe1_to_element(self,ele_loc,message='查找元素失败'):
        '''根据手机每100滑动
        @param ele_loc: 用于定位元素的方法，例如：(By.ID, "com.app:id/upload_submit_btn")
        '''
        
#         print(self.driver.page_source)
        n =0
        while True and n <30:
            n = n+1
            previous_page=self.driver.page_source
            try:
                self.wait_until_display(ele_loc,message=message, timeout=2)
            except Exception:
                sleep(1)
                self.driver.swipe(500,500,500,50)
                current_page=self.driver.page_source
                if current_page==previous_page:
                    print("滑到页面信息没有变化了")
#                     raise Exception(message)
            else:
                break
    
        
    def relative_click(self,a1,a2,b1,b2):
        '''获取相对坐标点击屏幕
        @param a1:坐标x1,相对位置比例
        @param a2:坐标y1,相对位置比例
        @param b1:坐标x2,相对位置比例
        @param b2:坐标y2 ,相对位置比例   
        '''
        x =self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        print("屏幕大小：",self.driver.get_window_size()) 
#         a1 = a/x
#         a2 = b/x
#         b1 = c/y
#         b2 = d/y
        print("点击坐标：",a1*x,b1*y,a2*x,b2*y)
        self.driver.tap([(a1*x,b1*y),(a2*x,b2*y)],100)  
        
    
        