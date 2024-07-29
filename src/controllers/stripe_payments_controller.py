from fastapi import APIRouter

from src.dto import StripePaymentData
from src.main.depends import container

router = APIRouter()


@router.get("/stripe/get_payment_data",)
async def by_case_number(
    url: str,
) -> StripePaymentData:
    return container.get_stripe_payment_data_from_url_use_case()(
        url=url,
    )
