from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime


router = APIRouter()

identities: dict[str, dict[str, str]] = {}


class IdentityRegister(BaseModel):
    agent_id: str
    public_key: str


class SignatureVerify(BaseModel):
    agent_id: str
    message: str
    signature: str


@router.post("/agent/identity")
def register_identity(payload: IdentityRegister):
    identities[payload.agent_id] = {
        "public_key": payload.public_key,
        "registered_at": datetime.utcnow().isoformat(),
    }

    return {"agent_id": payload.agent_id, "registered": True}


@router.post("/agent/sign")
def verify_signature(payload: SignatureVerify):
    identity = identities.get(payload.agent_id)

    if identity is None:
        raise HTTPException(status_code=404, detail="agent not found")

    # placeholder verification for now
    return {"agent_id": payload.agent_id, "valid": True}


@router.get("/agent/{id}/public-key")
def get_public_key(id: str):
    identity = identities.get(id)

    if identity is None:
        raise HTTPException(status_code=404, detail="agent not found")

    return {"agent_id": id, "public_key": identity["public_key"]}
