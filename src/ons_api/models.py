from pydantic import BaseModel
from typing import Optional

class PostFiltro(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    page: int = 1
    page_size: int = 50
    