from playwright.sync_api import sync_playwright
from scripting.site_modules.base_login import BaseLogin

class Login(BaseLogin):
    def login(self, proxy=None):
        with sync_playwright() as p:
            browser = p.firefox.launch(proxy={"server": proxy}, headless=True) if proxy else p.firefox.launch(headless=True)
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
                "cookies": self.process_cookies(cookies),
                "headers": {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'pl,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6',
                    'user-agent': user_agent
                }
            }
