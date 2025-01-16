from playwright.sync_api import sync_playwright
from MORE_JOBS.scripting.shop_modules.base_login import BaseLogin
import pdb

class Login(BaseLogin):
    def login(self, proxy=None):
        with sync_playwright() as p:
            browser = p.chromium.launch(proxy={"server": proxy}, headless=True) if proxy else p.chromium.launch(headless=False)
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
                "user_agent": user_agent
            }
