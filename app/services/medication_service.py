"""T-MED-1 (알약 인식 및 복약 스케줄 등록) — recognition_service.py(공통모듈)와 연동."""
from app.repositories.medication_repository import MedicationRepository


class MedicationService:
    def __init__(self, repository: MedicationRepository):
        self.repository = repository

    # TODO: 유스케이스 메서드 구현
