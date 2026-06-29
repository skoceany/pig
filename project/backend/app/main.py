from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.api.diagnosis import router as diagnosis_router
from app.api.disease import router as disease_router
from app.api.history import router as history_router
from app.config.settings import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diagnosis_router, prefix=settings.api_prefix)
app.include_router(disease_router, prefix=settings.api_prefix)
app.include_router(history_router, prefix=settings.api_prefix)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        content={"success": False, "message": "参数验证失败"},
        status_code=400
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        content={"success": False, "message": "服务器内部错误"},
        status_code=500
    )

@app.get("/")
async def root():
    return {"message": f"{settings.app_name} v{settings.app_version}"}