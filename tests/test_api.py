
import os
os.environ["QRNG_API_KEY"] = "test-secret-123"

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi.testclient import TestClient
from app.main import app

HEADERS = {"X-API-Key": "test-secret-123"}


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_qrng_returns_correct_count(client):
    resp = client.post("/v1/qrng", json={"bits": 64}, headers=HEADERS)
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] == 64
    assert len(data["bits"]) == 64
    assert set(data["bits"]) <= {"0", "1"}


def test_qrng_zero_bits(client):
    resp = client.post("/v1/qrng", json={"bits": 0}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json() == {"bits": "", "count": 0}


def test_negative_bits_rejected(client):
    resp = client.post("/v1/qrng", json={"bits": -1}, headers=HEADERS)
    assert resp.status_code == 422


def test_over_cap_rejected(client):
    resp = client.post("/v1/qrng", json={"bits": 1_000_000}, headers=HEADERS)
    assert resp.status_code == 422


def test_wrong_type_rejected(client):
    resp = client.post("/v1/qrng", json={"bits": "256"}, headers=HEADERS)
    assert resp.status_code == 422


def test_missing_field_rejected(client):
    resp = client.post("/v1/qrng", json={}, headers=HEADERS)
    assert resp.status_code == 422


def test_missing_api_key_rejected(client):
    resp = client.post("/v1/qrng", json={"bits": 16})
    assert resp.status_code in (401, 422)


def test_wrong_api_key_rejected(client):
    resp = client.post("/v1/qrng", json={"bits": 16}, headers={"X-API-Key": "wrong"})
    assert resp.status_code == 401


def test_output_passes_chi_square(client):
    resp = client.post("/v1/qrng", json={"bits": 5000}, headers=HEADERS)
    bits = resp.json()["bits"]

    from app.quantum import validate_randomness
    result = validate_randomness(bits)
    assert result["passed"], f"chi-square test failed: {result}"


def test_randomness_between_calls(client):
    resp1 = client.post("/v1/qrng", json={"bits": 128}, headers=HEADERS).json()["bits"]
    resp2 = client.post("/v1/qrng", json={"bits": 128}, headers=HEADERS).json()["bits"]
    assert resp1 != resp2, "Two consecutive calls returned identical bits -- suspicious!"
