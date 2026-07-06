from pydantic import BaseModel


class MedicationResponse(BaseModel):
    id: int
    drug_name: str

    class Config:
        from_attributes = True
