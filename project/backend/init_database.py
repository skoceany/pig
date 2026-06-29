import asyncio
import json
from sqlalchemy import select, func
from app.models.database import Base, DiseaseKnowledge, DiagnosisHistory
from app.config.database import engine, AsyncSessionLocal
from app.models.pig_disease_model import DISEASE_KNOWLEDGE

async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        count_result = await session.execute(
            select(func.count(DiseaseKnowledge.id))
        )
        count = count_result.scalar()
        
        if count == 0:
            for disease_name, info in DISEASE_KNOWLEDGE.items():
                disease = DiseaseKnowledge(
                    disease_name=disease_name,
                    description=info.get('description', ''),
                    symptoms=json.dumps(info.get('symptoms', [])),
                    transmission='',
                    treatment='',
                    prevention='',
                    images_count=0
                )
                session.add(disease)
            await session.commit()
            print("疾病知识库初始化完成")
        else:
            print("疾病知识库已存在，跳过初始化")

if __name__ == "__main__":
    asyncio.run(init_database())
