from fastapi import APIRouter
from pathlib import Path

router = APIRouter(prefix="/handshake", tags=["handshake"])

VERSION = Path("VERSION").read_text().strip()

@router.get("")
def handshake():
    return {
        "service": "hashr",
        "version": VERSION,
        "protocol": "x402",
        "ens": "hashr.eth",
        "node_type": "agent-service-node",
        "compatible_protocols": [
            "x402"
        ],
        "capabilities": [
            "compute",
            "jobs",
            "proof-verification",
            "wallet-risk",
            "reputation",
            "identity"
        ]
    }
