from abc import ABC, abstractmethod

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.dto import StripePaymentData
from src.third_parties.selenium_driver_factory import IDriverFactory


class IStripePaymentAdapter(ABC):
    @abstractmethod
    def get_payment_data_from_url(self, payment_url: str) -> StripePaymentData: ...


class SeleniumStripePaymentAdapter(IStripePaymentAdapter):

    def __init__(
        self,
        driver_factory: IDriverFactory,
    ) -> None:
        self.__driver_factory = driver_factory

    def get_payment_data_from_url(self, payment_url: str) -> StripePaymentData:
        with self.__driver_factory.start_driver() as driver:
            driver.get(payment_url)
            email_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ReadOnlyFormField-title")))
            email = email_element.text
            currency_amount = driver.find_element(By.CLASS_NAME, "CurrencyAmount").text
            return StripePaymentData(email=email, currency_amount=currency_amount)
