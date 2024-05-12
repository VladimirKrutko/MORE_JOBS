import json
import random
from time import sleep
from selenium import webdriver

class LoginScript:
    def __init__(self):
        self.proxy = random.choice(self.get_proxy())['proxy']

    def get_proxy(self):
        with open('http_proxies.json', 'r') as file:
            proxy = json.load(file)
        return proxy['proxies']
    
    def get_driver(self, proxy):
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument(f'--proxy-server={self.proxy}')
        return webdriver.Chrome()
    
    def new_session(self, driver):
        driver.quit()
        self.proxy = random.choice(self.get_proxy())['proxy']
        return self.get_driver(self.proxy.split('://')[1])
    
    def click_button_and_get_cookies(self, url):
        driver = self.get_driver(self.proxy)
        # while True:
        #     try:
        driver.get(url)
        #         # driver.find_element('xpath', '//div[@data-test="section-banner-details"]')
        #     except:
        #         driver = self.new_session(driver)
        #         continue
        #     sleep(7)
        #     try:
        #         while True:
        #             try:
        #                 driver.find_element('xpath', "//button[@data-test='button-submitCookie']")
        #                 break
        #             except:
        sleep(5)
        button = driver.find_element('xpath', "//button[@data-test='button-submitCookie']")
        #         print('Button found')
        #     except:
        #         driver = self.new_session(driver)
        #         print('Button not found')
        #         continue
        button.click()
        cookies = driver.get_cookies()
        driver.quit()
        return cookies
    
    def close(self):
        self.driver.quit()
        
    def get_cookies(self, url):
        cookies, proxy = self.click_button_and_get_cookies(url)
        cookies_dict = {}
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
        # return cookies_dict, proxy
        return { cookie['name']: cookie['value'] for cookie in cookies}