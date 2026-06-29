from fastapi import APIRouter, Path, Query
from fastapi.responses import JSONResponse
from app.services.history_service import HistoryService

router = APIRouter(prefix='/history', tags=['历史'])

@router.get('/')
async def get_history(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=50)):
    try:
        service = HistoryService()
        result = await service.get_history(page, size)
        return JSONResponse(content={"success": True, "data": result})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)},
            status_code=500
        )

@router.delete('/{record_id}')
async def delete_history(record_id: int = Path(...)):
    try:
        service = HistoryService()
        success = await service.delete_history(record_id)
        if success:
            return JSONResponse(content={"success": True, "message": "删除成功"})
        else:
            return JSONResponse(
                content={"success": False, "message": "记录不存在"},
                status_code=404
            )
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)},
            status_code=500
        )