from fastapi import APIRouter
from pathlib import Path

router = APIRouter(prefix="/health", tags=["health"])

VERSION = Path("VERSION").read_text().strip()


@router.get("")
def health():
    return {
        "status": "ok",
        "service": "hashr",
        "version": VERSION,
    }


@router.get("/ready")
def ready():
    return {
        "ready": True,
        "service": "hashr",
        "version": VERSION,
    }
