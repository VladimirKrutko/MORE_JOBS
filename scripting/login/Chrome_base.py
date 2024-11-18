import json
import random
from playwright.sync_api import sync_playwright
from base_login import BaseLogin

class PlaywrightLogin(BaseLogin):
    def login(self, proxy):
        with sync_playwright() as p:
            browser = p.chromium.launch(proxy={"server": proxy}, headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Переход на страницу логина (например, login_url)
            login_url = "https://it.pracuj.pl/praca"
            page.goto(login_url, timeout=60000)

            # Нажатие на кнопку принятия cookies
            page.locator("//button[@data-test=\"button-submitCookie\"]").click()
            page.wait_for_load_state("networkidle")
            
            # Извлекаем cookies и user agent
            cookies = context.cookies()
            user_agent = page.evaluate("() => navigator.userAgent")

            browser.close()

            return {
                "proxy": self.proxy,
                "cookies": cookies,
                "user_agent": user_agent
            }

# Использование

with open('proxy_list.json', 'r') as f:
    proxy_list = json.load(f)

valid_proxy = [proxy for proxy in proxy_list if not proxy['banned']]

login_instance = PlaywrightLogin()
for proxy in valid_proxy:
    
    try:
        credentials = login_instance.login(proxy['url'])
        break
    except Exception as e:
        print(e)
        continue
# credentials = login_instance.login( random.choice(valid_proxy).get('url'))
print(credentials)
