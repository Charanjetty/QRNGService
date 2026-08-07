# QRNG Service

A Quantum Random Number Generator (QRNG) REST API built with **FastAPI** and **Qiskit**.

The service generates random bits by simulating a single qubit using Qiskit's `AerSimulator`. Although the randomness comes from a quantum simulation rather than physical quantum hardware, the circuit and probability distribution faithfully represent a real quantum system.

---

## Live Demo

- **API:** https://qrngservice.onrender.com
- **Swagger Documentation:** https://qrngservice.onrender.com/docs
- **ReDoc Documentation:** https://qrngservice.onrender.com/redoc
- **GitHub Repository:** https://github.com/Charanjetty/QRNGService

---

## Features

- Generate quantum random bits using Qiskit
- REST API built with FastAPI
- API key authentication
- Automatic Swagger and ReDoc documentation
- Health check endpoint
- Randomness self-test using the Chi-Square test
- Docker support
- Unit tests with Pytest
- Deployable on Render

---

## Technology Stack

- Python
- FastAPI
- Qiskit
- Qiskit Aer
- Pydantic
- NumPy
- SciPy
- Pytest
- Docker

---

# Authentication

The QRNG endpoint requires an API key.

Use the following request header:

```http
X-API-Key: dev-key-for-local-testing
```

The API key is already configured on the deployed Render application for assignment evaluation.

---

# Running Locally

Clone the repository:

```bash
git clone https://github.com/Charanjetty/QRNGService.git

cd QRNGService
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set the API key:

Windows PowerShell

```powershell
$env:QRNG_API_KEY="dev-key-for-local-testing"
```

Linux/macOS

```bash
export QRNG_API_KEY=dev-key-for-local-testing
```

Run the application:

```bash
uvicorn app.main:app --reload
```

The API will be available at

```
http://127.0.0.1:8000
```

---

# Docker

Build:

```bash
docker build -t qrng-api .
```

Run:

```bash
docker run -p 8000:8000 -e QRNG_API_KEY=dev-key-for-local-testing qrng-api
```

---

# API Endpoints

## Home

```
GET /
```

Returns general information about the API.

---

## Health Check

```
GET /health
```

No authentication required.

Example response:

```json
{
    "status": "ok"
}
```

---

## Generate Random Bits

```
POST /v1/qrng
```

Authentication Required

Header

```
X-API-Key: dev-key-for-local-testing
```

Request

```json
{
    "bits": 256
}
```

Successful Response

```json
{
    "bits": "101001101001011001011001...",
    "count": 256
}
```

---

## Randomness Self-Test

```
GET /v1/qrng/self-test?n=256
```

Example response

```json
{
    "n": 256,
    "zeros": 129,
    "ones": 127,
    "chi_square": 0.015625,
    "p_value": 0.900524,
    "passed": true
}
```

---

# Using Swagger UI

Open

```
https://qrngservice.onrender.com/docs
```

1. Click **POST /v1/qrng**
2. Click **Try it out**
3. Enter the header:

```
X-API-Key
```

Value:

```
dev-key-for-local-testing
```

4. Enter a request body:

```json
{
  "bits": 128
}
```

5. Click **Execute**

The API returns a random binary string.

---

# Testing

Run

```bash
pytest -v
```

---

# Project Structure

```
QRNGService/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── quantum.py
│   └── security.py
│
├── tests/
│   └── test_api.py
│
├── requirements.txt
├── Dockerfile
├── runtime.txt
├── README.md
└── .gitignore
```

---

# Notes

- Randomness is produced using a simulated quantum circuit with Qiskit Aer.
- The free Render instance may take 30–60 seconds to respond after a period of inactivity due to cold starts.

---

# License

MIT