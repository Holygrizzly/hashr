from fastapi import APIRouter
from pathlib import Path

router = APIRouter(prefix="/pricing", tags=["pricing"])

VERSION = Path("VERSION").read_text().strip()


@router.get("")
def pricing():
    return {
        "service": "hashr",
        "version": VERSION,
        "pricing": {
            "compute": {
                "hash": 10,
                "search": 10,
                "inference": 10,
            },
            "jobs": {
                "create": 5,
                "execute": 10,
            },
            "proof": 5,
            "wallet-risk": 5,
            "reputation": 5,
            "identity-verification": 5,
            "contract-analysis": 10,
        },
        "currency": "credits",
    }
