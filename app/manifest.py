from fastapi import APIRouter

router = APIRouter(prefix="/manifest", tags=["manifest"])

@router.get("")
def get_manifest():
    return {
        "name": "hashr",
        "ens": "hashr.eth",
        "protocol": "x402",
        "version": "0.1",
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
