from __future__ import annotations

import asyncio
import hashlib
from typing import List

from fastapi import APIRouter, Header, Request
from pydantic import BaseModel

from .payment import verify_payment

router = APIRouter(prefix="/compute", tags=["compute"])


class HashRequest(BaseModel):
    text: str
    job_id: str | None = None


class HashResponse(BaseModel):
    job_id: str
    hash: str


class SearchRequest(BaseModel):
    query: str
    corpus: List[str]
    job_id: str | None = None


class SearchResponse(BaseModel):
    job_id: str
    matches: List[str]


class InferenceRequest(BaseModel):
    prompt: str
    model: str = "toy"
    job_id: str | None = None


class InferenceResponse(BaseModel):
    job_id: str
    output: str


async def _simulate_work():
    await asyncio.sleep(0.01)


@router.post("/hash", response_model=HashResponse)
async def compute_hash(
    payload: HashRequest,
    request: Request,
    x_402_payment: str | None = Header(None, alias="X-402-Payment"),
) -> HashResponse:
    verification = verify_payment(payload.job_id, request=request, x_402_payment=x_402_payment)

    await _simulate_work()
    digest = hashlib.sha256(payload.text.encode("utf-8")).hexdigest()
    return HashResponse(job_id=verification.job_id, hash=digest)


@router.post("/search", response_model=SearchResponse)
async def compute_search(
    payload: SearchRequest,
    request: Request,
    x_402_payment: str | None = Header(None, alias="X-402-Payment"),
) -> SearchResponse:
    verification = verify_payment(payload.job_id, request=request, x_402_payment=x_402_payment)

    await _simulate_work()
    hits = [doc for doc in payload.corpus if payload.query.lower() in doc.lower()]
    return SearchResponse(job_id=verification.job_id, matches=hits)


@router.post("/inference", response_model=InferenceResponse)
async def compute_inference(
    payload: InferenceRequest,
    request: Request,
    x_402_payment: str | None = Header(None, alias="X-402-Payment"),
) -> InferenceResponse:
    verification = verify_payment(payload.job_id, request=request, x_402_payment=x_402_payment)

    await _simulate_work()
    output = f"[{payload.model}] echoed: {payload.prompt}"
    return InferenceResponse(job_id=verification.job_id, output=output)
