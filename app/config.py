from pydantic import BaseModel


class PaymentSettings(BaseModel):
    price_credits: int = 10
    payment_address: str = "HASHR_DEMO_ADDRESS"


settings = PaymentSettings()
