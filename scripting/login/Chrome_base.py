import json
from playwright.sync_api import sync_playwright
from base_login import BaseLogin

class PlaywrightLogin(BaseLogin):
    def __init__(self):
        # Загрузка прокси из файла proxy_list.json
        with open('proxy_list.json', 'r') as f:
            proxy_list = json.load(f)
        valid_proxy = next((proxy for proxy in proxy_list if not proxy['banned']), None)
        self.proxy = valid_proxy.get('url') if valid_proxy else None
        
    def login(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(proxy={"server": self.proxy}, headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Переход на страницу логина (например, login_url)
            login_url = "https://it.pracuj.pl/praca"
            page.goto(login_url)

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
login_instance = PlaywrightLogin()
credentials = login_instance.login()
print(credentials)
