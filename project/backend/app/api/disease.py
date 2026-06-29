from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from app.services.knowledge_service import KnowledgeService

router = APIRouter(prefix='/disease', tags=['疾病'])

@router.get('/{disease_name}')
async def get_disease_info(disease_name: str = Path(...)):
    try:
        service = KnowledgeService()
        result = await service.get_disease_info(disease_name)
        if result:
            return JSONResponse(content={"success": True, "data": result})
        else:
            return JSONResponse(
                content={"success": False, "message": "疾病信息不存在"},
                status_code=404
            )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)},
            status_code=500
        )

@router.get('/')
async def get_all_diseases():
    try:
        service = KnowledgeService()
        diseases = await service.load_all_diseases()
        return JSONResponse(content={"success": True, "data": diseases})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)},
            status_code=500
        )