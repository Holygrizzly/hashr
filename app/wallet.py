from __future__ import annotations

import time

from fastapi import APIRouter, Request
from pydantic import BaseModel

from .payment import verify_payment

router = APIRouter(prefix="/wallet", tags=["wallet"])


class WalletRiskRequest(BaseModel):
    wallet: str
    job_id: str | None = None


@router.post("/risk")
async def wallet_risk_scan(payload: WalletRiskRequest, request: Request):
    """Placeholder wallet risk scoring.

    This is a machine-payable endpoint gated by x402; callers must include
    the payment header to pass verify_payment().
    """

    job_id = payload.job_id or payload.wallet
    await verify_payment(job_id=job_id, request=request)

    # Placeholder scoring logic derived from the wallet string.
    score = sum(ord(c) for c in payload.wallet) % 101
    sanctioned = score >= 92
    fraud_reports = 0 if score < 70 else 1

    return {
        "wallet": payload.wallet,
        "risk_score": score,
        "sanctioned": sanctioned,
        "fraud_reports": fraud_reports,
        "job_id": job_id,
        "timestamp": int(time.time()),
    }
