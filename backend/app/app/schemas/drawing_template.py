from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from app.schemas.response import Status

__all__ = [
    "DrawingTemplate",
    "DrawingTemplateCreate",
    "DrawingTemplateUpdate",
    "SuccessfulDrawingTemplateUpdateDeleteResponse",
    "DrawingTemplateGetList",
    "DrawingTemplateGet",
]


class DrawingTemplateBase(BaseModel):
    ownerSource: Optional[str] = None
    ownerId: Optional[str] = None
    name: Optional[str] = None
    tool: Optional[str] = None
    content: Optional[Dict[Any, Any]] = None


# Properties to receive on item creation
class DrawingTemplateCreate(DrawingTemplateBase):
    ownerSource: str
    ownerId: str
    name: str
    tool: str
    content: Dict[Any, Any]


# Properties to receive on item update
class DrawingTemplateUpdate(DrawingTemplateBase):
    pass


# Properties shared by models stored in DB
class DrawingTemplateInDBBase(DrawingTemplateBase):
    class Config:
        orm_mode = True

    id: int
    ownerSource: str
    ownerId: str
    name: str
    tool: str
    content: Dict[Any, Any]


# Properties to return to client
class DrawingTemplate(DrawingTemplateInDBBase):
    class Config:
        orm_mode = True


class SuccessfulDrawingTemplateUpdateDeleteResponse(BaseModel):
    status: Status = Field(Status.ok)


class DrawingTemplateGetList(BaseModel):
    name: str


class DrawingTemplateGet(BaseModel):
    name: str
    content: Dict[Any, Any]
