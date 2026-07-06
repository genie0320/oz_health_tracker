from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.medication_repository import MedicationRepository
from app.services.medication_service import MedicationService

router = APIRouter()


def get_service(db: AsyncSession = Depends(get_db)) -> MedicationService:
    return MedicationService(MedicationRepository(db))


@router.get("/ping")
async def ping():
    return {"domain": "medication", "status": "scaffold-ok"}
