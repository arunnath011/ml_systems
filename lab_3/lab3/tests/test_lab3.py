import os
import sys
import pytest
import json
from fastapi.testclient import TestClient
from lab3.main import app, HousingDataInputList, model , HousingDataOutput,BlockGroup
from pydantic import ValidationError
import joblib
import requests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


client = TestClient(app)

import redis

redis_client = redis.Redis(host='localhost', port=6379)


def test_predict_with_valid_data():
    valid_data = {"data": [
        {"MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.98412698, "AveBedrms": 1.02380952, "Population": 322,
         "AveOccup": 2.55555556, "Latitude": 37.88, "Longitude": -122.23}]}
    cache_key = json.dumps(valid_data)

    # check if result is in Redis cache
    if redis_client.exists(cache_key):
        result = json.loads(redis_client.get(cache_key))
        assert result['predictions'] is not None
    else:
        # execute the request and cache the result in Redis
        response = client.post("/predict", json=valid_data)
        assert response.status_code == 200
        result = response.json()
        redis_client.set(cache_key, json.dumps(result))

    # check the result
    assert result['predictions'] is not None


def test_hello_endpoint():
    response = requests.get("http://localhost:8000/hello?name=test_user")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello test_user"}


def test_hello_endpoint_with_no_name():
    response = requests.get("http://localhost:8000/hello")
    assert response.status_code == 400
    assert response.json() == {"detail": "Name not specified"}


def test_root_endpoint():
    response = requests.get("http://localhost:8000/")
    assert response.status_code == 501
    assert response.json() == {"detail": "Not Implemented"}


def test_docs_endpoint():
    response = requests.get("http://localhost:8000/docs")
    assert response.status_code == 200


def test_openapi_endpoint():
    response = requests.get("http://localhost:8000/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()


def test_hello_endpoint_with_long_name():
    long_name = "a" * 250
    response = requests.get(f"http://localhost:8000/hello?name={long_name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello {long_name[:250]}"}


def test_hello_endpoint_with_special_characters_name():
    special_characters_name = "!@#$%^&*()"
    response = requests.get(f"http://localhost:8000/hello?name={special_characters_name}")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello !@"}


def test_numbers_endpoint():
    # Test valid input
    response = requests.get("http://localhost:8000/numbers?num=10")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

    # Test input with decimals
    response = requests.get("http://localhost:8000/numbers?num=10.5")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

    # Test input with negative numbers
    response = requests.get("http://localhost:8000/numbers?num=-10")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}

    # Test input without number
    response = requests.get("http://localhost:8000/numbers")
    assert response.status_code == 404
    if isinstance(response.json()["detail"], str):
        error_message = response.json()["detail"]
    else:
        error_messages = [error_message["msg"] for error_message in response.json()["detail"]]
    assert "Not Found" in error_message




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

# def test_predict_mismatched_order():
#     invalid_data = {"data": [{"MedInc": 8.3252, "AveBedrms": 1.02380952, "AveRooms": 6.98412698, "Latitude": 37.88, "AveOccup": 2.55555556, "Population": 322, "HouseAge": 41.0, "Longitude": -122.23}]}
#     response = client.post("/predict", json=invalid_data)
#     assert response.status_code == 422

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_load_model():
    assert model is not None