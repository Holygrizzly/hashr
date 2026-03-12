from fastapi import APIRouter, Request, Header
from pathlib import Path
from web3 import Web3
import os

from .payment import verify_payment

router = APIRouter(prefix="/contract", tags=["contracts"])

VERSION = Path("VERSION").read_text().strip()

RPC_URL = os.getenv("ETH_RPC_URL", "https://rpc.ankr.com/eth")
w3 = Web3(Web3.HTTPProvider(RPC_URL))


@router.post("/analyze")
def analyze_contract(
    payload: dict,
    request: Request,
    x_402_payment: str | None = Header(None, alias="X-402-Payment"),
):
    verify_payment(job_id="contract_analyze", request=request, x_402_payment=x_402_payment)

    address = payload.get("address")

    if not address:
        return {"error": "contract address required"}

    code = w3.eth.get_code(address).hex()

    has_code = code != "0x"
    code_size = len(code)

    proxy_pattern = "delegatecall" in code.lower()
    owner_pattern = "owner" in code.lower()

    honeypot_pattern = False

    suspicious_patterns = [
        "transferfrom",
        "revert",
        "require",
    ]

    for pattern in suspicious_patterns:
        if pattern in code.lower():
            honeypot_pattern = True
            break

    risk_score = 0

    if not has_code:
        risk_score += 50

    if proxy_pattern:
        risk_score += 25

    if owner_pattern:
        risk_score += 10

    if honeypot_pattern:
        risk_score += 40

    if risk_score >= 50:
        risk_level = "high"
    elif risk_score >= 20:
        risk_level = "medium"
    else:
        risk_level = "low"

    flags = {
        "no_code": not has_code,
        "proxy_pattern": proxy_pattern,
        "ownership_pattern": owner_pattern,
        "honeypot_pattern": honeypot_pattern,
    }

    return {
        "service": "hashr",
        "version": VERSION,
        "analysis": {
            "address": address,
            "has_code": has_code,
            "code_size": code_size,
            "proxy_pattern_detected": proxy_pattern,
            "ownership_pattern_detected": owner_pattern,
            "honeypot_pattern_detected": honeypot_pattern,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "flags": flags,
            "status": "basic-security-analysis",
        },
    }
