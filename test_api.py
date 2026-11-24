"""
Integration Tests for FastAPI Microservice Endpoints
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.api.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert data["version"] == "1.0.0"

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert data["models_loaded"]["forecaster"] is True

def test_model_info_endpoint(client):
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert data["lookback_window"] == 14
    assert data["n_features"] == 15

def test_predict_sales_valid_payload(client):
    payload = {
        "history_sales": [1200.0, 1350.0, 1100.0, 1450.0, 1600.0, 1800.0, 1950.0,
                          1250.0, 1300.0, 1400.0, 1550.0, 1650.0, 1850.0, 2100.0],
        "is_weekend": 1,
        "day_of_week": 5,
        "month": 12
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_sales" in data
    assert data["predicted_sales"] >= 0.0
    assert len(data["confidence_interval_80"]) == 2
    assert "X-Process-Time-Ms" in response.headers

def test_predict_sales_invalid_length(client):
    # Only 5 values provided instead of mandatory 14
    payload = {
        "history_sales": [1200.0, 1350.0, 1100.0, 1450.0, 1600.0],
        "is_weekend": 0
    }
    response = client.post("/predict", json=payload)
    # Pydantic validation error HTTP 422
    assert response.status_code == 422

def test_predict_churn_endpoint(client):
    payload = {
        "tenure": 36,
        "monthly_charges": 60.0,
        "total_charges": 2160.0,
        "contract": "One year",
        "payment_method": "Credit card (automatic)",
        "paperless_billing": "No",
        "senior_citizen": 0
    }
    response = client.post("/predict_churn", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "churn_probability" in data
    assert 0.0 <= data["churn_probability"] <= 1.0
    assert data["risk_level"] in ["LOW RISK", "MEDIUM RISK", "HIGH RISK"]
