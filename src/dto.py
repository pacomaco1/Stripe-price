from dataclasses import dataclass


@dataclass
class StripePaymentData:
    email: str
    currency_amount: str
