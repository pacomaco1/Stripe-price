from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from src.adapters.stripe_payment_adapter import SeleniumStripePaymentAdapter
from src.third_parties.selenium_driver_factory import DriverFactory
from src.usecases.get_sripe_payment_data_from_url_use_case import GetStripePaymentDataFromUrlUseCase


class Container(DeclarativeContainer):
    driver_factory = providers.Factory(
        DriverFactory,
    )
    stripe_payment_adapter = providers.Factory(
        SeleniumStripePaymentAdapter,
        driver_factory=driver_factory,
    )
    get_stripe_payment_data_from_url_use_case = providers.Factory(
        GetStripePaymentDataFromUrlUseCase,
        stripe_payment_adapter=stripe_payment_adapter,
    )


container = Container()
