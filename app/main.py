from fastapi import FastAPI

from .compute import router as compute_router
from .jobs import router as jobs_router
from .payment import router as payment_router
from .reputation import router as reputation_router
from .proof import router as proof_router
from .wallet import router as wallet_router
from .identity import router as identity_router
from .manifest import router as manifest_router
from .health import router as health_router
from .capabilities import router as capabilities_router
from .pricing import router as pricing_router
from .registry import router as registry_router


app = FastAPI(
    title="hashr",
    version="0.1.0",
    description="Machine-payable compute server that uses the x402 payment protocol.",
)


app.include_router(payment_router)
app.include_router(compute_router)
app.include_router(jobs_router)
app.include_router(reputation_router)
app.include_router(proof_router)
app.include_router(wallet_router)
app.include_router(identity_router)
app.include_router(manifest_router)
app.include_router(health_router)
app.include_router(capabilities_router)
app.include_router(pricing_router)
app.include_router(registry_router)


@app.get("/")
def root():
    """Simple service metadata and protocol hint."""
    return {
        "service": "hashr",
        "protocol": "x402",
        "manifest": "/manifest",
        "discovery": "/.well-known/hashr",
        "ens": "hashr.eth",
        "openapi": "/openapi.json",
    }
