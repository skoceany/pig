import asyncio
from sqlalchemy import select, func
from app.models.database import Base, DiseaseKnowledge
from app.config.database import engine, AsyncSessionLocal
from app.utils.data_loader import load_disease_descriptions

async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        count_result = await session.execute(
            select(func.count(DiseaseKnowledge.id))
        )
        count = count_result.scalar()
        if count == 0:
            diseases = load_disease_descriptions("../../多模态数据/train-data")
            for disease in diseases:
                session.add(DiseaseKnowledge(**disease))
            await session.commit()
            print("疾病知识库初始化完成")

if __name__ == "__main__":
    asyncio.run(init_database())