from pydantic import BaseModel, Field
from typing import Optional

class PostFilter(BaseModel):
    start_date: str = Field(..., description="Start date (dd-mm-yyyy)", example="01-01-2023")
    end_date: Optional[str] = Field(None, description="Data final no formato dd-mm-yyyy", example="31-01-2023")
    