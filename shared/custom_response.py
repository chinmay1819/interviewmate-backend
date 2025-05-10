from typing import Any, Optional
from pydantic import BaseModel

class CustomResponse(BaseModel):
    status_code: int
    message: str
    result: Optional[Any] = None 
