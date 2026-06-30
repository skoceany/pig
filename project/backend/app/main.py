import logging
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.api.diagnosis import router as diagnosis_router
from app.api.disease import router as disease_router
from app.api.history import router as history_router
from app.config.settings import settings
from app.config.database import engine, Base, AsyncSessionLocal

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动/关闭时的生命周期管理"""
    # === 启动时 ===
    # 1. 创建 uploads 目录
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"上传目录已就绪: {upload_dir.absolute()}")

    # 2. 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("数据库表已创建/确认")

    # 3. 初始化疾病知识库数据（如果为空）
    await _init_knowledge_base()
    logger.info("疾病知识库已初始化")

    yield  # 应用运行中

    # === 关闭时 ===
    await engine.dispose()
    logger.info("数据库连接已清理")


async def _init_knowledge_base():
    """如果疾病知识库表为空，则初始化内置数据"""
    from sqlalchemy import select, func
    from app.models.database import DiseaseKnowledge
    from app.models.pig_disease_model import _FALLBACK_DISEASE_INFO

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(func.count(DiseaseKnowledge.id)))
        count = result.scalar()
        if count > 0:
            return  # 已有数据，跳过

        for name, info in _FALLBACK_DISEASE_INFO.items():
            import json
            record = DiseaseKnowledge(
                disease_name=name,
                description=info.get("description", ""),
                symptoms=json.dumps(info.get("symptoms", []), ensure_ascii=False),
                transmission=info.get("transmission", ""),
                treatment=info.get("treatment", ""),
                prevention=info.get("prevention", ""),
            )
            session.add(record)
        await session.commit()
        logger.info(f"知识库已初始化 {len(_FALLBACK_DISEASE_INFO)} 条疾病数据")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

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

@app.get("/")
async def root():
    return {"message": f"{settings.app_name} v{settings.app_version}"}