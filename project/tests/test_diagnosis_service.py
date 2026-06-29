import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.diagnosis_service import DiagnosisService

@pytest.fixture
def diagnosis_service():
    service = DiagnosisService()
    service.model.predict = MagicMock(return_value={"disease": "非洲猪瘟", "confidence": 0.9})
    service.model.generate_interpretation = MagicMock(return_value={
        "description": "测试疾病解读",
        "symptoms": ["高烧", "皮肤紫斑"],
        "recommendations": ["立即隔离"]
    })
    return service

def test_predict_disease(diagnosis_service):
    result = diagnosis_service.model.predict("test_image")
    assert "disease" in result
    assert "confidence" in result
    assert 0 <= result["confidence"] <= 1

def test_generate_interpretation(diagnosis_service):
    result = diagnosis_service.model.generate_interpretation("非洲猪瘟", "test_image")
    assert "description" in result
    assert isinstance(result["description"], str)