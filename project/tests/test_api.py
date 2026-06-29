import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "猪病诊断智能体" in response.json()["message"]

def test_disease_info_api():
    response = client.get("/api/disease/非洲猪瘟")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True

def test_get_all_diseases():
    response = client.get("/api/disease/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True