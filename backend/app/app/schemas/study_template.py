from typing import Optional, Dict, Any, Any

from pydantic import BaseModel, Field


from app.schemas.response import Status

__all__ = [
    "StudyTemplate",
    "StudyTemplateCreate",
    "StudyTemplateUpdate",
    "SuccessfulStudyTemplateUpdateDeleteResponse",
    "StudyTemplateGetList",
    "StudyTemplateGet",
]


class StudyTemplateBase(BaseModel):
    ownerSource: Optional[str] = None
    ownerId: Optional[str] = None
    name: Optional[str] = None
    content: Optional[Dict[Any, Any]] = None


# Properties to receive on item creation
class StudyTemplateCreate(StudyTemplateBase):
    ownerSource: str
    ownerId: str
    name: str
    content: Dict[Any, Any]


# Properties to receive on item update
class StudyTemplateUpdate(StudyTemplateBase):
    pass


# Properties shared by models stored in DB
class StudyTemplateInDBBase(StudyTemplateBase):
    class Config:
        orm_mode = True

    id: int
    ownerSource: str
    ownerId: str
    name: str
    content: Dict[Any, Any]


# Properties to return to client
class StudyTemplate(StudyTemplateInDBBase):
    class Config:
        orm_mode = True


class SuccessfulStudyTemplateUpdateDeleteResponse(BaseModel):
    status: Status = Field(Status.ok)


class StudyTemplateGetList(BaseModel):
    name: str


class StudyTemplateGet(BaseModel):
    name: str
    content: Dict[Any, Any]
