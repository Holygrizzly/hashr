from fastapi import FastAPI

from .compute import router as compute_router
from .jobs import router as jobs_router
from .payment import router as payment_router
from .reputation import router as reputation_router


app = FastAPI(
    title="hashr",
    version="0.1.0",
    description="Machine-payable compute server that uses the x402 payment protocol.",
)

app.include_router(payment_router)
app.include_router(compute_router)
app.include_router(jobs_router)
app.include_router(reputation_router)


@app.get("/")
def root():
    """Simple service metadata and protocol hint."""
    return {"service": "hashr", "protocol": "x402"}
