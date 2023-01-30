# test_app.py
import requests

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


