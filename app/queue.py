from fastapi import APIRouter
from pathlib import Path

router = APIRouter(prefix="/queue", tags=["queue"])

VERSION = Path("VERSION").read_text().strip()


@router.get("")
def queue_status():
    return {
        "service": "hashr",
        "version": VERSION,
        "queue": {
            "pending_jobs": "placeholder",
            "active_jobs": "placeholder",
            "completed_jobs": "placeholder",
        },
    }
