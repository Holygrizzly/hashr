from fastapi import APIRouter
from pathlib import Path
import time

router = APIRouter(prefix="/metrics", tags=["metrics"])

VERSION = Path("VERSION").read_text().strip()

START_TIME = time.time()

@router.get("")
def metrics():
    uptime = int(time.time() - START_TIME)
    return {
        "service": "hashr",
        "version": VERSION,
        "uptime_seconds": uptime,
        "status": "running",
        "metrics": {
            "requests_total": "placeholder",
            "jobs_total": "placeholder",
            "proofs_verified": "placeholder",
        },
    }
