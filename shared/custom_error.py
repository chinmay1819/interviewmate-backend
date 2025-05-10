from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import HTTPException

class CustomError(BaseModel):
    status_code: int
    message: str
    error: Optional[str] = None


def raise_custom_error(status_code: int, message: str, error: Optional[str] = None):
    raise HTTPException(
        status_code=status_code,
        detail={
            "status_code": status_code,
            "message": message,
            "error": error
        }
    )
