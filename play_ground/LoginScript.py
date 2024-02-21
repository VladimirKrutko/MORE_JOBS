from time import sleep
from selenium import webdriver

class LoginScript:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def click_button_and_get_cookies(self, url):
        self.driver.get(url)
        sleep(7)
        button = self.driver.find_element('xpath', "//button[@data-test='button-submitCookie']")
        button.click()
        cookies = self.driver.get_cookies()
        return cookies
    
    def close(self):
        self.driver.quit()
        
    def get_cookies(self, url):
        cookies = self.click_button_and_get_cookies(url)
        self.close()
        cookies_dict = {}
        for cookie in cookies:
            cookies_dict[cookie['name']] = cookie['value']
        return cookies_dict
        # return { cookie['name']: cookie['value'] for cookie in cookies}