'''
Created on 2018年8月8日

@author: geqiuli
'''
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import NoSuchElementException
import re
import os
import base64
import hashlib
from selenium.common.exceptions import TimeoutException
from PIL import Image
from localplugins.PredictCaptcha import predict_captcha

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('BASE_DIR: ',BASE_DIR)

class Base:
    '''driver的一些基础封装'''
    
    def __init__(self,driver):
        self.driver=driver
        
    def wait_until_display(self, ele_loc,timeout=30):
        '''
        @param ele_loc: 元素定位方法，类似： (By.ID, "bu", "元素描述语")
        '''
        message='查找元素超时: '+str(ele_loc)
        WebDriverWait(self.driver,timeout).until(EC.visibility_of_element_located(ele_loc[:2]),message=message)
    
    def wait_until_display_any(self, ele_loc, timeout=30):
        '''
        @param ele_loc: 元素定位方法，类似： (By.ID, "bu", "元素描述语")
        '''
        message='查找元素超时: '+str(ele_loc)
        WebDriverWait(self.driver,timeout).until(EC.visibility_of_any_elements_located(ele_loc[:2]),message=message)
    
    def wait_until_undisplay(self, ele_loc, timeout=30):
        '''
        @param ele_loc: 元素定位方法，类似： (By.ID, "bu", "元素描述语")
        '''
        message='页面仍然显示元素: '+str(ele_loc)
        WebDriverWait(self.driver,timeout).until(EC.invisibility_of_element_located(ele_loc[:2]),message=message)
    
    def wait_until_text_display(self, ele_loc, text, timeout=30):
        '''
        @param ele_loc: 元素定位方法，类似： (By.ID, "bu", "元素描述语")
        '''
        msg='指定元素中未显示文字：'+text
        WebDriverWait(self.driver,timeout).until(EC.text_to_be_present_in_element((ele_loc[:2],text)),message=msg)        
    
    def wait_title_contains(self, target_title, timeout=30):
        '''
        @param ele_loc: 元素定位方法，类似： (By.ID, "bu", "元素描述语")
        '''
        message='页面没有跳转到: '+target_title
        WebDriverWait(self.driver,timeout).until(EC.title_contains((target_title)),message=message)
    
    def wait_until_clickable(self, ele_loc, ele_desc=None, timeout=30):
        '''
        @param ele_loc: 元素定位方法，类似： (By.ID, "bu", "元素描述语")
        '''
        if ele_desc:
            message=str(ele_desc)+': 元素不可点击'
        else:
            message=str(ele_loc)+': 元素不可点击'
        self.wait_until_display(ele_loc,timeout)
        WebDriverWait(self.driver,timeout).until(EC.element_to_be_clickable(ele_loc[:2]),message=message)
                    
    
    def find_element(self, ele_loc,timeout=30):
        '''查找元素
        @param ele_loc: 元素定位方法，类似： (By.ID, "bu", "元素描述语")
        '''
        try:
            self.wait_until_display(ele_loc,timeout)
            ele=self.driver.find_element(*ele_loc[:2])
            return ele
        except NoSuchElementException:
            msg='查找元素超时：'+str(ele_loc)
            print(msg)
            raise Exception(msg)
        except TimeoutException:
            msg='查找元素超时：'+str(ele_loc)
            print(msg)
            raise Exception(msg)
        except Exception as e:
            print('其他异常')
            raise Exception(e)
    
    def find_elements(self, ele_loc,timeout=30):
        '''查找元素
        @param loc: 元素定位方法，类似： (By.ID, "bu")
        @param ele_desc: 元素描述'''
        try:
            WebDriverWait(self.driver,timeout).until(EC.visibility_of_any_elements_located(ele_loc[:2]),message='timeout')
            ele=self.driver.find_elements(*ele_loc[:2])
            return ele
        except NoSuchElementException:
            msg='查找元素超时：'+str(ele_loc)
            print(msg)
            return [] 
        except TimeoutException:
            msg='查找元素超时：'+str(ele_loc)
            print(msg)
            return []    
        except Exception as e:
            print('其他异常： ',e)
            return []   
    
    def find_child_use_ele(self, father_ele, children_loc):
        '''
        @param father_ele: 父元素'''
        try:
            child_ele=father_ele.find_element(*children_loc[:2])
            return child_ele
        except NoSuchElementException:
            msg='查找元素超时：'+str(children_loc)
            print(msg)
            return []    
        except Exception as e:
            print('其他异常')
            raise Exception(e)  
        
    def find_child_use_loc(self, father_loc, children_loc):
        '''
        @param father_loc: 父元素定位方式'''
        try:
            WebDriverWait(self.driver,30).until(EC.visibility_of_any_elements_located(father_loc[:2]),message='timeout')
            father_ele=self.driver.find_element(*father_loc[:2])
        except NoSuchElementException:
            msg='查找元素超时：'+str(father_loc)
            print(msg)
            return []    
        except Exception as e:
            print('其他异常')
            raise Exception(e)
        else:
            try:
                child_ele=father_ele.find_element(*children_loc[:2])
                return child_ele
            except NoSuchElementException:
                msg='查找元素超时：'+str(children_loc)
                print(msg)
                return []    
            except Exception as e:
                print('其他异常')
                raise Exception(e)
                  
        
    def switch_to_latest_windows(self):
        """
        浏览器多窗口，切换到最新窗口
        """
        handles = self.driver.window_handles  # 获取所有窗口句柄
        if len(handles)>1:
            self.driver.switch_to.window(handles[-1])  # 切换到最新窗口
        else:
            print('当前只有一个窗口，不切换窗口')
            

    def get_page_source(self):
        """
        获取当前页面源码
        :return:
        """
        page_source = self.driver.page_source
        return page_source

    def assert_source(self, text):
        """
        断言当前页面源码是否包含字段
        :param text:
        :return:
        """
        src = self.get_page_source()
        text_found = re.search(text, src)
        assert (text_found is not None)
    
    
    # 重新封装输入方法
    def send_keys(self, loc, value, clear_first=True, click_first=True):
        """
        输入方法，默认清空输入框，并点击，再输入
        :param loc: 传递的loc必须为R对象中的tuple，而不是WebElement对象
        :param value:
        :param clear_first:
        :param click_first:
        :return:
        """
        try:
            if click_first:
                self.find_element(loc).click()
            if clear_first:
                self.find_element(loc).clear()
            self.find_element(loc).send_keys(value)
        except AttributeError:
            print(u"%s 页面未能找到 %s 元素" % (self, loc))

    # 重新封装按钮点击方法
    def click(self, loc, find_first=True):
        """
        按钮点击
        :param loc: 传递的loc必须为R对象中的tuple，而不是WebElement对象
        :param find_first:
        :return:
        """
        try:
            if find_first:
                self.find_element(loc[:2])
            self.find_element(loc[:2]).click()
        except AttributeError:
            print(u"%s 页面未能找到 %s 按钮" % (self, loc))

    def click_element(self, ele_loc, timeout=30):
        '''点击元素，点击前判断：是否显示、是否可点击'''
        self.wait_until_clickable(ele_loc[:2], timeout)
        self.find_element(ele_loc).click()

    def get_last_window_title(self):
        """
        浏览器多窗口，获取最新窗口标题
        :return:
        """
        handles = self.driver.window_handles  # 获取所有窗口句柄
        current_handle = self.driver.current_window_handle  # 保存当前窗口句柄
        self.driver.switch_to.window(handles[-1])  # 切换到弹出窗口
        title = self.driver.title  # 获取标题
        self.driver.switch_to.window(current_handle)  # 切换回原窗口
        return title

    def close_latest_window(self):
        """
        浏览器多窗口，关闭最后一个窗口
        :return:
        """
        handles = self.driver.window_handles  # 获取所有窗口句柄
        self.driver.switch_to.window(handles[-1])  # 切换到弹出窗口
        self.driver.close()  # 关闭
        self.driver.switch_to.window(handles[-2])  # 切换回上一个窗口

    def switch_frame(self, index=0):
        """
        切换到页面Frame
        :param index: Frame索引，从0开始
        :return:
        """
        self.driver.switch_to.frame(index)

    @classmethod
    def get_file_path(cls, file):
        """
        获取文件路径
        :param file: 文件相对路径
        :return: 文件绝对路径
        """
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), file))
        # DEBUG
        # print(path)
        return path

    @classmethod
    def decode_password(cls, password_string):
        base64_byte = base64.b64decode(password_string)
        md5_object = hashlib.md5()
        md5_object.update(base64_byte)
        # Debug
        # print(md5_object.hexdigest())
        x = md5_object.hexdigest()[:6]
        return x

    def get_current_url(self):
        return self.driver.current_url
        
    def get_page_title(self):
        """
        获取页面标题
        :param selenium:
        :return:
        """
        print('The page title is:%s' % self.driver.title)
        return self.driver.title

    def isElementExist(self,webelement) :
        '''
        判断元素会是否存在
        @author:chenpeng
        :param webelement:
        :return:
        '''
        try :
            self.find_element(webelement)
            return True
        except :
            return False
        
    def get_image_captcha(self,image_name,captcha_name,captcha_ele,captcha_type):
        """
    保存验证码图片至本地供识别
    @param image_name: 截图名称
    @param captcha_name: 从截图裁剪下来的验证码图片名称
    @param captcha_ele: 验证码图片的元素定位
    @param captcha_type: 验证码颜色类型：colorful-彩色；   blackwhite-黑白；
        @return:识别出来的验证码
        """
        #image_name='screenshot_b2bapp_findpassword.png'
        image_path=os.path.join(BASE_DIR,'localplugins','captcha', 'images',image_name)
        #captcha_name='captcha_b2bapp_findpassword.png'
        captcha_path=os.path.join(BASE_DIR,'localplugins','captcha', 'images',captcha_name)
        
        self.driver.save_screenshot(image_path)
        
        captcha_element = self.find_element(captcha_ele, timeout=10) #验证码图片
        #print(captcha.location)
        #print(captcha.size)
        left = captcha_element.location['x']
        top = captcha_element.location['y']
        right = captcha_element.location['x'] + captcha_element.size['width']
        bottom = captcha_element.location['y'] + captcha_element.size['height']
        
        im = Image.open(image_path)
        im = im.crop((left, top, right, bottom))
        im = im.resize((100,40),Image.ANTIALIAS)    #修改尺寸
        im.save(captcha_path)
        captcha_text = predict_captcha(captcha_type,captcha_name) 
        print('智能识别的验证码为；',captcha_text)
        return captcha_text  
        
        
        