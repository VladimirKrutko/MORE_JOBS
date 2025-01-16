from abc import ABC, abstractmethod

class BaseLogin(ABC):
    @abstractmethod
    def login(self):
        return {
            "proxy": None,
            "cookies": None,
            "user_agent": None
        }
    
    def process_cookies(self, cookies):
        return "; ".join([f"{cook['name']}={cook['value']}" for cook in cookies])