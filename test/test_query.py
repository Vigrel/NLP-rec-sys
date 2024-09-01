from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_yields_10_results():
    response = client.get("/query?query=A dark drink for the halloween")
    json_response = response.json()
    
    assert response.status_code == 200
    assert len(json_response["results"]) == 10
    assert json_response["message"] == "OK"

def test_query_yields_few_results():
    response = client.get("/query?query=I'd like a drink with that reminds me some smoky notes due the heavy weather of today")
    json_response = response.json()
    
    assert response.status_code == 200
    assert 1 < len(json_response["results"]) < 10
    assert json_response["message"] == "OK"

def test_query_yields_non_obvious_results():
    response = client.get("/query?query=Perfect drink pairings for a burger")
    json_response = response.json()
    """The non-obvious result is due to the fact
    that the author of the drinks is called Jake Burger """
    # TODO: add assert to verify non obvious results
    assert response.status_code == 200
    assert len(json_response["results"]) > 0
    assert json_response["message"] == "OK"
