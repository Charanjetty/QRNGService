# QRNG Service

## About the Project

This project is a **Quantum Random Number Generator (QRNG)** built using **FastAPI** and **Qiskit**. It generates random bits by simulating a quantum circuit with a Hadamard gate and measurement, then exposes the functionality through a REST API.

> **Note:** This project uses Qiskit's **AerSimulator**, which simulates a quantum computer. It does not use real quantum hardware.

---

## Live Demo

**Live API:**

**GitHub Repository:** https://github.com/Charanjetty/QRNGService

---

## Features

* Generate quantum random bits through a REST API
* Health check endpoint
* Chi-square statistical self-test
* API key authentication
* Input validation with FastAPI and Pydantic
* Clear error responses
* Unit tests using pytest

---

## Project Structure

```text
qrng-service/
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
├── README.md
├── .gitignore
└── .dockerignore
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Charanjetty/QRNGService.git
cd QRNGService
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Set the API key.

### Windows PowerShell

```powershell
$env:QRNG_API_KEY="dev-key-for-local-testing"
```

Start the server:

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Generate Random Bits

**POST** `/v1/qrng`

Request:

```json
{
  "bits": 256
}
```

Response:

```json
{
  "bits": "1101001010111100...",
  "count": 256
}
```

---

### Health Check

**GET** `/health`

Response:

```json
{
  "status": "ok"
}
```

---

### Self-Test

**GET** `/v1/qrng/self-test?n=5000`

Example response:

```json
{
  "n": 5000,
  "zeros": 2498,
  "ones": 2502,
  "chi_square": 0.0032,
  "p_value": 0.954889
}
```

---

## Example Request

### cURL

```bash
curl -X POST http://127.0.0.1:8000/v1/qrng \
-H "Content-Type: application/json" \
-H "X-API-Key: dev-key-for-local-testing" \
-d "{\"bits\":256}"
```

### Python

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/v1/qrng",
    json={"bits": 256},
    headers={"X-API-Key": "dev-key-for-local-testing"},
)

print(response.json())
```

---

## Running Tests

```bash
pytest
```

---

## My Approach

I started by implementing the function that generates random bits using a quantum circuit in Qiskit. Once that was working, I created a FastAPI endpoint so users could request random bits through a REST API.

Adding request validation and API key authentication was straightforward because FastAPI provides these features out of the box.

The biggest challenge was debugging the statistical self-test. At first, the endpoint returned an internal server error. I used the error messages and tested different inputs to find the issue in the chi-square calculation. After fixing it, the endpoint returned the expected statistics.

Another challenge was deployment. I also ran into storage limitations on my local machine while trying to use Docker. I solved this by preparing the application for deployment on a cloud platform.

This project helped me understand how to combine quantum computing concepts with web development, testing, and API deployment.

---

## License

MIT
