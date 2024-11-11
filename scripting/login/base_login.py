from abc import ABC, abstractmethod

class BaseLogin(ABC):
    @abstractmethod
    def login(self):
        """
        Метод для логина, который должен возвращать словарь с ключами 'proxy', 'cookies', 'user_agent'.
        """
        return {
            "proxy": None,
            "cookies": None,
            "user_agent": None
        }