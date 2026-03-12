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

    return {
        "service": "hashr",
        "version": VERSION,
        "analysis": {
            "address": address,
            "code_size": len(code),
            "has_code": code != "0x",
            "status": "basic-analysis",
            "note": "advanced security checks not implemented yet",
        },
    }
