from pathlib import Path
from datetime import datetime
from app.models.pig_disease_model import PigDiseaseModel
from app.models.database import DiagnosisHistory
from app.utils.image_utils import save_image, preprocess_image
from app.config.settings import settings
from app.config.database import AsyncSessionLocal

class DiagnosisService:
    def __init__(self):
        self.model = PigDiseaseModel()

    async def diagnose(self, image_file):
        image_path = await self._save_uploaded_image(image_file)
        processed_image = preprocess_image(image_path)
        prediction = self.model.predict(processed_image)
        interpretation = self.model.generate_interpretation(
            prediction['disease'],
            processed_image
        )

        result = {
            'is_sick': prediction['confidence'] > settings.confidence_threshold,
            'disease_name': prediction['disease'],
            'confidence': prediction['confidence'],
            'interpretation': interpretation.get('description', ''),
            'symptoms': interpretation.get('symptoms', []),
            'recommendations': interpretation.get('recommendations', [])
        }

        await self._save_history(image_path, result)
        return result

    async def _save_uploaded_image(self, image_file):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{timestamp}_{image_file.filename}'
        save_path = Path(settings.upload_dir) / filename
        await save_image(image_file, save_path)
        return str(save_path)

    async def _save_history(self, image_path, result):
        history = DiagnosisHistory(
            image_path=image_path,
            disease_name=result['disease_name'],
            confidence=result['confidence'],
            interpretation=result['interpretation'],
            symptoms=str(result['symptoms']),
            recommendations=str(result['recommendations'])
        )
        async with AsyncSessionLocal() as session:
            session.add(history)
            await session.commit()