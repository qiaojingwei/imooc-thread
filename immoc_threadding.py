# coding:utf-8
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
import xlrd
import xlwt
import threading
from imooc_get_info import *
global ALL_HANDLES

def get_ele_wait(driver,time,func):
    return WebDriverWait(driver,time).until(func)
# 打开浏览器
def openBrowser():
    return webdriver.Firefox()
# 打开慕课网
# def openUrl(driver):
#     driver.get('https://www.imooc.com/')
#     time.sleep(1)

def find_web_ele(driver):
    get_ele_wait(driver,100,lambda driver:driver.find_element_by_id('js-signin-btn')).click() #点击登录按钮
    time.sleep(2)
    get_ele_wait(driver,10,lambda driver: driver.find_element_by_class_name('icon-qq')).click() #选择qq作为登录方式，此时打开的是两个窗口
    ALL_HANDLES = driver.window_handles
    driver.switch_to_window(ALL_HANDLES[1])
    driver.maximize_window()
    time.sleep(2)
    driver.switch_to.frame(0)
    time.sleep(1)
    get_ele_wait(driver,10,lambda driver: driver.find_element_by_id('switcher_plogin')).click() #选择使用账号密码登录
    qq_usr = get_ele_wait(driver,10,lambda driver: driver.find_element_by_class_name('inputstyle'))
    qq_pwd = get_ele_wait(driver,10,lambda driver: driver.find_element_by_id('p'))
    ok_login = get_ele_wait(driver,10,lambda driver: driver.find_element_by_id('login_button'))
    return qq_usr,qq_pwd,ok_login

def imooc_login_and_choice_class(driver,usr_info):
    idx = 10
    while idx > 0:
        try:
            ele_tuple = find_web_ele(driver)
        except Exception as e:
            print(str(e))
        else:
            break
        finally:
            time.sleep(1)
            idx = idx - 1
    ele_tuple[0].send_keys('123')
    ele_tuple[0].clear()
    ele_tuple[0].send_keys(usr_info['usrname'])
    ele_tuple[1].send_keys('')
    ele_tuple[1].clear()
    ele_tuple[1].send_keys(usr_info['password'])
    ele_tuple[2].click()

    ALL_HANDLES = driver.window_handles
    driver.switch_to_window(ALL_HANDLES[0])
    time.sleep(2)
    idx = 10
    try:
        while idx > 0:
            if True == choice_job(driver):
                break
            time.sleep(1)
            idx = idx - 1
    except:
        pass
    imooc_logout(driver)

def choice_job(driver):
    driver.find_element_by_link_text('运维&测试').click()
    time.sleep(1)
    ALL_HANDLES = driver.window_handles
    driver.switch_to_window(ALL_HANDLES[1])
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div[1]/div/div[3]/a/div[1]/img').click() #选择课程
    time.sleep(3)
    ALL_HANDLES = driver.window_handles
    driver.switch_to_window(ALL_HANDLES[2])
    driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div[4]/div/div/span').click() #收藏课程
    return Ture
def imooc_logout(driver):
    ALL_HANDLES = driver.window_handles
    for i in range(1,len(ALL_HANDLES)):
        driver.switch_to_window(ALL_HANDLES[i])
        driver.close()
    driver.switch_to_window(ALL_HANDLES[0])
    ActionChains(driver).move_to_element(driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/ul/li[4]/a/img')).perform()
    time.sleep(3)
    ActionChains(driver).move_to_element(driver.find_element_by_link_text('安全退出')).click().perform()

def imooc_test(usr_info,uri):
    driver = openBrowser()
    driver.get(uri)
    time.sleep(1)
    imooc_login_and_choice_class(driver,usr_info)
    driver.quit()
if __name__ == '__main__':
    usr_list = get_usr_info(r'F:\PyProjects\imooc\imooc_info.xlsx')
    uri = r'https://www.imooc.com/'
    for usr_info in usr_list:
        t = threading.Thread(target=imooc_test, args=(usr_info,uri))  # 创建线程
        #t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程


    # while True:
    #     time.sleep(10)
