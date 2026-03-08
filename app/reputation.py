from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

agents: Dict[str, Dict[str, Any]] = {}


class RegisterAgent(BaseModel):
    id: str
    reputation: int = 0


class ReputationQuery(BaseModel):
    id: str


@router.post("/agent/register")
def register_agent(payload: RegisterAgent):
    agents[payload.id] = {
        "reputation": payload.reputation,
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }
    return {"agent_id": payload.id, **agents[payload.id]}


@router.post("/reputation/query")
def query_reputation(payload: ReputationQuery):
    agent = agents.get(payload.id)
    if agent is None:
        raise HTTPException(status_code=404, detail="agent not found")
    return {"agent_id": payload.id, "reputation": agent.get("reputation")}


@router.get("/agent/{id}")
def get_agent(id: str):
    agent = agents.get(id)
    if agent is None:
        raise HTTPException(status_code=404, detail="agent not found")
    return {"agent_id": id, **agent}
