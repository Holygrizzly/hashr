from __future__ import annotations

import uuid
from dataclasses import dataclass

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel

from .config import settings

router = APIRouter(prefix="/payment", tags=["payment"])


class PaymentQuote(BaseModel):
    job_id: str
    price: float
    payment_address: str


@dataclass
class PaymentVerification:
    job_id: str
    payment_token: str


def quote_price(job_id: str | None) -> PaymentQuote:
    """Return a placeholder price quote for the given job."""

    if job_id is None:
        job_id = uuid.uuid4().hex

    return PaymentQuote(
        job_id=job_id,
        price=settings.price_credits,
        payment_address=settings.payment_address,
    )


def verify_payment(
    job_id: str | None,
    request: Request,
    x_402_payment: str | None = Header(None, alias="X-402-Payment"),
) -> PaymentVerification:
    """Placeholder x402 verification.

    If no token is provided, raise HTTP 402 with the quote payload.
    Otherwise, accept any token as valid for now.
    """

    quote = quote_price(job_id)

    if not x_402_payment:
        # FastAPI's HTTPException detail can be any JSON-serializable object.
        raise HTTPException(status_code=402, detail=quote.model_dump())

    return PaymentVerification(job_id=quote.job_id, payment_token=x_402_payment)


@router.get("/quote/{job_id}", response_model=PaymentQuote)
async def get_quote(job_id: str) -> PaymentQuote:
    return quote_price(job_id)


class PaymentVerificationPayload(BaseModel):
    payment_token: str


@router.post("/verify/{job_id}")
async def verify_endpoint(job_id: str, payload: PaymentVerificationPayload) -> dict:
    # Placeholder: we would verify payload.payment_token against x402 payments.
    return {"job_id": job_id, "verified": True}
