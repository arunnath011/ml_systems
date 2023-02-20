import os
import sys
import pytest
import json
from fastapi.testclient import TestClient
from src.main import app, HousingDataInputList, model , HousingDataOutput,BlockGroup
from pydantic import ValidationError
import joblib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


client = TestClient(app)

def test_predict_with_valid_data():
    valid_data = {"data": [{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}]}
    response = client.post("/predict", json=valid_data)
    assert response.status_code == 200

def test_predict_empty_input():
    test_data_empty = {
        "data": []
    }
    response = client.post("/predict", json=test_data_empty)
    assert response.status_code == 200
    assert response.json() == {"predictions": []}


def test_predict_with_missing_field():
    invalid_data = {"data": [{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556}]}
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422

def test_predict_with_invalid_data():
    invalid_data = {"data": [{"MedInc": "not a number", "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}]}
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422

def test_predict_invalid_population():
    invalid_data = {"data": [{"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 0, "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}]}
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422

def test_predict_mismatched_order():
    invalid_data = {"data": [{"MedInc": 8.3252, "AveBedrms": 1.02380952, "AveRooms": 6.98412698, "Latitude": 37.88, "AveOccup": 2.55555556, "Population": 322, "HouseAge": 41.0, "Longitude": -122.23}]}
    response = client.post("/predict", json=invalid_data)
    assert response.status_code == 422

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_load_model():
    assert model is not None