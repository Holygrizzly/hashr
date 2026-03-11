from pathlib import Path
from fastapi import APIRouter

VERSION = Path("VERSION").read_text().strip()

router = APIRouter(prefix="/manifest", tags=["manifest"])


@router.get("")
def get_manifest():
    return {
        "name": "hashr",
        "ens": "hashr.eth",
        "protocol": "x402",
        "version": VERSION,
        "capabilities": [
            "compute",
            "jobs",
            "proof-verification",
            "wallet-risk",
            "reputation",
            "identity",
        ],
        "endpoints": {
            "compute": "/compute",
            "jobs": "/job",
            "proof": "/proof",
            "wallet": "/wallet",
            "reputation": "/reputation",
            "identity": "/agent",
        },
    }
