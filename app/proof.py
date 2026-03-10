from __future__ import annotations

import hashlib
import time
from typing import Dict

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from .payment import verify_payment

router = APIRouter(prefix="/proof", tags=["proof"])


class ProofVerifyRequest(BaseModel):
    job_id: str
    input_hash: str
    output_hash: str
    worker_agent: str


ProofRecord = Dict[str, object]
proofs: Dict[str, ProofRecord] = {}


def _proof_payload_hash(job_id: str, input_hash: str, output_hash: str, worker_agent: str) -> str:
    data = f"{job_id}:{input_hash}:{output_hash}:{worker_agent}".encode()
    return hashlib.sha256(data).hexdigest()


@router.post("/verify")
async def verify_proof(request: Request, proof_req: ProofVerifyRequest):
    await verify_payment(job_id=proof_req.job_id, request=request)

    proof_hash = _proof_payload_hash(
        proof_req.job_id,
        proof_req.input_hash,
        proof_req.output_hash,
        proof_req.worker_agent,
    )
    record: ProofRecord = {
        "job_id": proof_req.job_id,
        "verified": True,
        "proof_hash": proof_hash,
        "timestamp": int(time.time()),
        "worker_agent": proof_req.worker_agent,
    }
    proofs[proof_req.job_id] = record
    return record


@router.get("/{job_id}")
async def get_proof(request: Request, job_id: str):
    await verify_payment(job_id=job_id, request=request)

    record = proofs.get(job_id)
    if not record:
        raise HTTPException(status_code=404, detail="Proof not found")
    return record
