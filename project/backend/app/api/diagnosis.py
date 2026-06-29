from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from app.services.diagnosis_service import DiagnosisService

router = APIRouter(prefix='/diagnosis', tags=['诊断'])

@router.post('/')
async def diagnose(image: UploadFile = File(...)):
    try:
        service = DiagnosisService()
        result = await service.diagnose(image)
        return JSONResponse(content={"success": True, "data": result})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)},
            status_code=500
        )