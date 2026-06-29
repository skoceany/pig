from sqlalchemy import select, func
from app.models.database import DiagnosisHistory
from app.config.database import AsyncSessionLocal

class HistoryService:
    async def get_history(self, page, size):
        async with AsyncSessionLocal() as session:
            offset = (page - 1) * size
            total_result = await session.execute(
                select(func.count(DiagnosisHistory.id))
            )
            total = total_result.scalar()

            result = await session.execute(
                select(DiagnosisHistory)
                .order_by(DiagnosisHistory.created_at.desc())
                .offset(offset)
                .limit(size)
            )
            records = result.scalars().all()

            return {
                'records': [self._to_dict(record) for record in records],
                'total': total,
                'page': page,
                'size': size
            }

    async def delete_history(self, record_id):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(DiagnosisHistory).where(DiagnosisHistory.id == record_id)
            )
            record = result.scalar_one_or_none()
            if record:
                await session.delete(record)
                await session.commit()
                return True
            return False

    def _to_dict(self, record):
        return {
            'id': record.id,
            'image_path': record.image_path,
            'disease_name': record.disease_name,
            'confidence': record.confidence,
            'interpretation': record.interpretation,
            'symptoms': record.symptoms,
            'recommendations': record.recommendations,
            'created_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }