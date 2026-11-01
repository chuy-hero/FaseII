from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_inicio():
    response = client.get("/")
    assert response.status_code == 200
    assert "API de detección de fraude activa" in response.json()["mensaje"]

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_prediccion_valida():
    response = client.post("/predict", json={
        "monto": 999, "hora": 1, "pais_riesgoso": 1
    })
    assert response.status_code == 200
    assert response.json()["prediccion"] in [0, 1]
    assert 0 <= response.json()["probabilidad_fraude"] <= 1

def test_rechaza_monto_no_valido():
    response = client.post("/predict", json={
        "monto": -1, "hora": 1, "pais_riesgoso": 0
    })
    assert response.status_code == 422

def test_rechaza_hora_fuera_de_rango():
    response = client.post("/predict", json={
        "monto": 200, "hora": 25, "pais_riesgoso": 0
    })
    assert response.status_code == 422
