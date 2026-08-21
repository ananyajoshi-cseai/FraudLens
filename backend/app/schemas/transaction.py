from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    user_id: str = Field(..., example="U1001")
    amount: float = Field(..., gt=0, example=18500)
    beneficiary_id: str = Field(..., example="B999")
    beneficiary_name: str = Field(..., example="Unknown Entity")
    transaction_hour: int = Field(..., ge=0, le=23, example=2)
    device_id: str = Field(..., example="DEV-NEW-88")
    failed_attempts: int = Field(..., ge=0, example=2)