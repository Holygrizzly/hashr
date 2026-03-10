from __future__ import annotations

import uuid
from typing import Any, Dict

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel

from .payment import verify_payment

router = APIRouter(prefix="/job", tags=["jobs"])


class JobCreate(BaseModel):
    payload: Dict[str, Any] | None = None


class Job(BaseModel):
    id: str
    status: str
    payload: Dict[str, Any] | None = None


JOBS: Dict[str, Job] = {}


@router.post("/", response_model=Job)
async def create_job(job: JobCreate) -> Job:
    job_id = uuid.uuid4().hex
    new_job = Job(id=job_id, status="created", payload=job.payload or {})
    JOBS[job_id] = new_job
    return new_job


@router.get("/{job_id}", response_model=Job)
async def get_job(job_id: str) -> Job:
    job = JOBS.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/{job_id}/execute", response_model=Job)
async def execute_job(
    job_id: str,
    request: Request,
    x_402_payment: str | None = Header(None, alias="X-402-Payment"),
) -> Job:
    verify_payment(job_id=job_id, request=request, x_402_payment=x_402_payment)

    job = JOBS.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    job.status = "completed"
    JOBS[job_id] = job
    return job
