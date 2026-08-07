from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.quantum import generate_random_bits, validate_randomness
from app.security import verify_api_key

MAX_BITS_PER_REQUEST = 100_000

app = FastAPI(
    title="QRNG Service",
    description="A quantum random number generator API, backed by a simulated qubit (Qiskit).",
    version="1.0.0",
)


# Request / Response Models


class QRNGRequest(BaseModel):
    bits: int = Field(
        ...,
        ge=0,
        le=MAX_BITS_PER_REQUEST,
        description=f"Number of random bits to generate (0-{MAX_BITS_PER_REQUEST})",
    )


class QRNGResponse(BaseModel):
    bits: str
    count: int


# Root Endpoint

@app.get("/")
def root():
    return {
        "service": "QRNG Service",
        "version": "1.0.0",
        "description": "Quantum Random Number Generator API using FastAPI and Qiskit.",
        "endpoints": {
            "documentation": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "generate_random_bits": "/v1/qrng",
            "self_test": "/v1/qrng/self-test",
            "openapi_schema": "/openapi.json",
        },
    }

# Generate Random Bits

@app.post("/v1/qrng", response_model=QRNGResponse)
def get_random_bits(
    payload: QRNGRequest,
    api_key: str = Depends(verify_api_key),
):
    bits = generate_random_bits(payload.bits)
    return QRNGResponse(bits=bits, count=len(bits))


# Health Check


@app.get("/health")
def health():
    return {"status": "ok"}

# Self-Test

@app.get("/v1/qrng/self-test")
def self_test(n: int = 5000):
    if n <= 0 or n > MAX_BITS_PER_REQUEST:
        raise HTTPException(
            status_code=422,
            detail=f"n must be between 1 and {MAX_BITS_PER_REQUEST}",
        )

    bits = generate_random_bits(n)
    return validate_randomness(bits)


# Global Exception Handler

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error. Please try again or contact support."
        },
    )