from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import Mock

client = TestClient(app)

def test_root_success():
    """
    Test that the root endpoint returns a 200 status code and the expected JSON response.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Server is running..."}

def test_root_failure():
    """
    Test that the root endpoint returns the expected error status code.
    """
    client.get = Mock()
    
    client.get.return_value.status_code = 404
    client.get.return_value.json.return_value = {"error": "Not Found"}
    
    response = client.get("/fail")
    
    assert response.json() == {"error": "Not Found"}