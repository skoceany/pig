import json
from sqlalchemy import select
from app.models.database import DiseaseKnowledge
from app.config.database import AsyncSessionLocal

class KnowledgeService:
    async def get_disease_info(self, disease_name):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(DiseaseKnowledge).where(DiseaseKnowledge.disease_name == disease_name)
            )
            disease = result.scalar_one_or_none()
            if disease:
                return {
                    'disease_name': disease.disease_name,
                    'description': disease.description,
                    'symptoms': json.loads(disease.symptoms) if disease.symptoms else [],
                    'transmission': disease.transmission,
                    'treatment': disease.treatment,
                    'prevention': disease.prevention
                }
            return None

    async def load_all_diseases(self):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(DiseaseKnowledge.disease_name)
            )
            return [row[0] for row in result]