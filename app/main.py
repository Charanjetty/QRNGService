
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.quantum import generate_random_bits
from app.security import verify_api_key
from fastapi import Depends

MAX_BITS_PER_REQUEST = 100_000

app = FastAPI(
    title="QRNG Service",
    description="A quantum random number generator API, backed by a simulated qubit (Qiskit).",
    version="1.0.0",
)

#Request like what we get from client .
class QRNGRequest(BaseModel):
    bits: int = Field(
        ...,
        ge=0,
        le=MAX_BITS_PER_REQUEST,
        description=f"Number of random bits to generate (0-{MAX_BITS_PER_REQUEST})",
    )

#Response in which structure we havee to send
class QRNGResponse(BaseModel):
    bits: str
    count: int


@app.post("/v1/qrng", response_model=QRNGResponse)
def get_random_bits(payload: QRNGRequest, api_key: str = Depends(verify_api_key)):
    bits = generate_random_bits(payload.bits)
    return QRNGResponse(bits=bits, count=len(bits))


@app.get("/health")
def health():
    return {"status": "ok"}

from app.quantum import validate_randomness

@app.get("/v1/qrng/self-test")
def self_test(n: int = 5000):
    if n <= 0 or n > MAX_BITS_PER_REQUEST:
        raise HTTPException(status_code=422, detail=f"n must be between 1 and {MAX_BITS_PER_REQUEST}")
    bits = generate_random_bits(n)
    return validate_randomness(bits)

from fastapi import Request
from fastapi.responses import JSONResponse


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again or contact support."},
    )
