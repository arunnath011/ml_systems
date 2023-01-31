# test_app.py
import requests

def test_hello_endpoint():
    response = requests.get("http://localhost:8000/hello?name=test_user")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello test_user"}
    
def test_hello_endpoint_with_no_name():
    response = requests.get("http://localhost:8000/hello")
    assert response.status_code==400
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
