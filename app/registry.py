from fastapi import APIRouter
from pathlib import Path

router = APIRouter(prefix="/registry", tags=["registry"])

VERSION = Path("VERSION").read_text().strip()

@router.get("")
def registry():
    return {
        "service": "hashr",
        "version": VERSION,
        "routes": [
            "/compute/hash",
            "/compute/search",
            "/compute/inference",
            "/job",
            "/job/{id}",
            "/job/{id}/execute",
            "/proof/verify",
            "/proof/{job_id}",
            "/wallet/risk",
            "/reputation/query",
            "/reputation/erc8004",
            "/agent/register",
            "/agent/{id}",
            "/agent/identity",
            "/agent/sign",
            "/agent/{id}/public-key",
        ],
    }
