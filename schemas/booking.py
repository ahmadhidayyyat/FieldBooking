from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BookingBase(BaseModel):
    field_name: str = Field(..., min_length=1, max_length=100)
    start_time: Optional[datetime] = None
    end_time: datetime

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
