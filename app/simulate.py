from fastapi import APIRouter
from pathlib import Path
from web3 import Web3
import os

router = APIRouter(prefix="/simulate", tags=["simulation"])

VERSION = Path("VERSION").read_text().strip()

RPC_URL = os.getenv("ETH_RPC_URL", "https://rpc.ankr.com/eth")
w3 = Web3(Web3.HTTPProvider(RPC_URL))

@router.post("/transaction")
def simulate_transaction(payload: dict):
    tx = payload.get("tx")

    try:
        result = w3.eth.call(tx)
        return {
            "service": "hashr",
            "version": VERSION,
            "simulation": {
                "status": "success",
                "result": result.hex(),
            },
        }

    except Exception as e:
        return {
            "service": "hashr",
            "version": VERSION,
            "simulation": {
                "status": "error",
                "error": str(e),
            },
        }
