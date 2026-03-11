from fastapi import APIRouter
from pathlib import Path

router = APIRouter(prefix="/job-descriptor", tags=["jobs"])

VERSION = Path("VERSION").read_text().strip()

@router.get("")
def job_descriptor():
    return {
        "service": "hashr",
        "version": VERSION,
        "job_schema": {
            "create_job": {
                "endpoint": "/job",
                "method": "POST",
                "payload": {
                    "payload": "object",
                },
            },
            "execute_job": {
                "endpoint": "/job/{id}/execute",
                "method": "POST",
                "requires_payment": True,
            },
        },
        "supported_compute": [
            "/compute/hash",
            "/compute/search",
            "/compute/inference",
        ],
    }
