from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix='/chat', tags=['对话'])

@router.post('/')
async def chat(message: str = Body(..., embed=True)):
    try:
        service = ChatService()
        response = await service.chat(message)
        return JSONResponse(content={"success": True, "data": {"response": response}})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)},
            status_code=500
        )

@router.post('/history')
async def chat_with_history(messages: list = Body(...)):
    try:
        service = ChatService()
        response = await service.chat_with_history(messages)
        return JSONResponse(content={"success": True, "data": {"response": response}})
    except Exception as e:
        return JSONResponse(
            content={"success": False, "message": str(e)},
            status_code=500
        )