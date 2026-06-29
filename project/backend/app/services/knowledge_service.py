import json
from sqlalchemy import select
from app.models.database import DiseaseKnowledge
from app.config.database import AsyncSessionLocal
from app.models.pig_disease_model import DISEASE_KNOWLEDGE

class KnowledgeService:
    async def get_disease_info(self, disease_name):
        db_result = await self._get_from_database(disease_name)
        if db_result:
            return db_result
        
        return self._get_from_knowledge(disease_name)

    async def _get_from_database(self, disease_name):
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

    def _get_from_knowledge(self, disease_name):
        info = DISEASE_KNOWLEDGE.get(disease_name)
        if info:
            return {
                'disease_name': disease_name,
                'description': info.get('description', ''),
                'symptoms': info.get('symptoms', []),
                'transmission': '',
                'treatment': '',
                'prevention': '',
                'recommendations': info.get('recommendations', [])
            }
        return None

    async def load_all_diseases(self):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(DiseaseKnowledge.disease_name)
            )
            db_diseases = [row[0] for row in result]
        
        knowledge_diseases = list(DISEASE_KNOWLEDGE.keys())
        all_diseases = list(set(db_diseases + knowledge_diseases))
        all_diseases.sort()
        return all_diseases
