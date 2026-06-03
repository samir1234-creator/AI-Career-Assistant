from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel

DataT = TypeVar('DataT')

class BaseResponse(BaseModel, Generic[DataT]):
    success: bool
    data: Optional[DataT] = None
    message: Optional[str] = None
