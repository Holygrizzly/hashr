from fastapi import APIRouter
from pathlib import Path

router = APIRouter(prefix="/simulate", tags=["simulation"])

VERSION = Path("VERSION").read_text().strip()

@router.post("/transaction")
def simulate_transaction(payload: dict):
    return {
        "service": "hashr",
        "version": VERSION,
        "simulation": {
            "status": "placeholder",
            "message": "transaction simulation not implemented yet",
            "input": payload,
        },
    }
