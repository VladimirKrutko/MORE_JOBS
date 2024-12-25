from playwright.sync_api import sync_playwright
from scripting.crawler import BaseLogin

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