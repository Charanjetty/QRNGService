
import os
from fastapi import Header, HTTPException

API_KEY = os.environ.get("QRNG_API_KEY", "dev-only-insecure-key")


def verify_api_key(x_api_key: str = Header(...)):
    # FastAPI dependency: reads the 'X-API-Key' header and checks it.
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return x_api_key
