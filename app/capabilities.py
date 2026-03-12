from fastapi import APIRouter
from pathlib import Path

router = APIRouter(prefix="/capabilities", tags=["capabilities"])

VERSION = Path("VERSION").read_text().strip()


@router.get("")
def capabilities():
    return {
        "service": "hashr",
        "version": VERSION,
        "capabilities": [
            "compute",
            "jobs",
            "proof-verification",
            "wallet-risk",
            "reputation",
            "identity",
            "contract-analysis",
        ],
    }
