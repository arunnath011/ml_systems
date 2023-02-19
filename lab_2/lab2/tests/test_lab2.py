import os
import sys
import pytest
import json
from fastapi.testclient import TestClient
from src.main import app, HousingDataInput, model , HousingDataOutput
from pydantic import ValidationError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import joblib

client = TestClient(app)

# Define test cases
test_data = {
    "data": [[8.3252, 41.0, 6.98412698, 1.02380952, 322.0, 2.55555556, 37.88, -122.23],
             [8.3014, 21.0, 5.90755981, 0.97188049, 496.0, 2.48544521, 37.85, -122.24]]
}

# Test cases
def test_predict():
    response = client.post("/predict", json=test_data)
    assert response.status_code == 200
    assert len(response.json()['predictions']) == 2
    assert len(response.json()['predictions'][0]) == 1


def test_invalid_input():
    invalid_data = {
        "data": [[8.3252, 41.0, 6.98412698, 1.02380952, 322.0, 2.55555556, "invalid", -122.23],
                 [8.3014, 21.0, 5.90755981, 0.97188049, 496.0, 2.48544521, 37.85, -122.24]]
    }
    response = client.post("/predict", data=json.dumps(invalid_data))
    assert response.status_code == 422
    assert "float" in response.json()["detail"][0]["msg"]

def test_predict_empty_input():
    test_data_empty = {
        "data": [[]]
    }
    response = client.post("/predict", json=test_data_empty)
    assert response.status_code == 200
    assert response.json() == {"predictions": []}



def test_predict_invalid_input_value():
    invalid_data = test_data.copy()
    invalid_data["data"][0][0] = "invalid"  # set first value of first row to a non-float value
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422
    #assert response.json() == {"detail": [{"loc": ["body", "data"], "msg": "field required", "type": "value_error.missing"}]}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_load_model():
    assert model is not None
