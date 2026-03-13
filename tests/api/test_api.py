from fastapi.testclient import TestClient
from hybrid_cse_system_v2.api.app import app, get_ml_models


class MockModels:
    def predict(self, text: str):
        return {
            "prediction": "spam",
            "score": 0.99,
            "reasons": ["mock rule triggered"]
        }


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json()["status"] == "okay"


def test_root_endpoint():
    with TestClient(app) as client:
        response = client.get("/")

        assert response.status_code == 200
        assert "CSE Detection API running" in response.json()["message"]


def test_analyse_endpoint():

    # Override dependency with mock model
    app.dependency_overrides[get_ml_models] = lambda: MockModels()

    payload = {
        "text": "Claim your free prize now https://fakebank.xyz"
    }

    with TestClient(app) as client:
        response = client.post("/analyse", json=payload)

    # Clear override after test
    app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "score" in data
    assert "reasons" in data

    assert isinstance(data["prediction"], str)
    assert isinstance(data["score"], float)
    assert isinstance(data["reasons"], list)
