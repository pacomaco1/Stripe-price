from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.adapters.stripe_payment_adapter import IStripePaymentAdapter
from src.dto import StripePaymentData


@dataclass(frozen=True)
class IGetStripePaymentDataFromUrlUseCase(ABC):
    @abstractmethod
    def __call__(self, url: str) -> StripePaymentData: ...


@dataclass(frozen=True)
class GetStripePaymentDataFromUrlUseCase(IGetStripePaymentDataFromUrlUseCase):

    stripe_payment_adapter: IStripePaymentAdapter

    def __call__(self, url: str) -> StripePaymentData:
        return self.stripe_payment_adapter.get_payment_data_from_url(payment_url=url)
