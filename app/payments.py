from fastapi import APIRouter
from pathlib import Path

router = APIRouter(prefix="/payments", tags=["payments"])

VERSION = Path("VERSION").read_text().strip()

@router.get("")
def payments():
    return {
        "service": "hashr",
        "version": VERSION,
        "protocol": "x402",
        "payment_header": "X-402-Payment",
        "payment_model": "per-request",
        "payment_endpoints": [
            "/compute/hash",
            "/compute/search",
            "/compute/inference",
            "/job/{id}/execute",
            "/proof/verify",
            "/proof/{job_id}",
            "/wallet/risk",
        ],
    }
