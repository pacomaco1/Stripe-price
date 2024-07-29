from abc import ABC, abstractmethod
from collections.abc import Generator
from contextlib import contextmanager

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium_stealth import stealth


class IDriverFactory(ABC):

    @contextmanager
    @abstractmethod
    def start_driver(self) -> Generator[WebDriver, None, None]:
        pass


class DriverFactory(IDriverFactory):

    def __init__(self, headless: bool = True) -> None:
        self._driver: WebDriver | None = None
        self.headless = headless

    @contextmanager
    def start_driver(self) -> Generator[WebDriver, None, None]:
        try:
            if self._driver is None:
                self._driver = self.__get_driver()
            yield self._driver
        finally:
            self._close_driver()

    def _close_driver(self) -> None:
        if self._driver:
            self._driver.quit()
            self._driver = None

    def __get_options(self) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-web-security')
        options.add_argument("--lang=en-US")
        prefs = {
            "profile.default_content_settings.popups": 0,
            "profile.default_content_setting_values.cookies": 1,
            "profile.cookie_controls_mode": 0,
            }
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        if self.headless:
            options.add_argument('--headless=new')
        return options

    def __get_driver(self) -> WebDriver:
        chrome_options = self.__get_options()
        driver = webdriver.Chrome(options=chrome_options)
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        driver.maximize_window()
        return driver
