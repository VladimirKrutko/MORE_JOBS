import json
import random
from playwright.sync_api import sync_playwright
from base_login import BaseLogin

class PlaywrightLogin(BaseLogin):
    def login(self, proxy=None):
        with sync_playwright() as p:
            browser = p.chromium.launch(proxy={"server": proxy}, headless=False) if proxy else p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            login_url = "https://it.pracuj.pl/praca"
            page.goto(login_url, timeout=60000)
            page.locator("//button[@data-test=\"button-submitCookie\"]").click()
            page.wait_for_load_state("networkidle")
            cookies = context.cookies()
            user_agent = page.evaluate("() => navigator.userAgent")
            browser.close()
            return {
                "proxy": proxy,
                "cookies": cookies,
                "user_agent": user_agent
            }

# with open('proxy_list.json', 'r') as f:
#     proxy_list = json.load(f)

# valid_proxy = [proxy for proxy in proxy_list if not proxy['banned']]

login_instance = PlaywrightLogin()
# for proxy in valid_proxy:
    
#     try:
#         credentials = login_instance.login(proxy['url'])
#         break
#     except Exception as e:
#         print(e)
#         continue
credentials = login_instance.login()
print(credentials)
