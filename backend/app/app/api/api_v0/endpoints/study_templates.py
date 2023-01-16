import json
from typing import Any, Optional, Dict, Union, List

from fastapi import APIRouter, Depends, HTTPException, status, Query, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.schemas.response import Status, SuccessfulResponse

router = APIRouter()


@router.post("/", response_model=schemas.SuccessfulStudyTemplateUpdateDeleteResponse)
async def create_update_study_template(
    *,
    db: AsyncSession = Depends(deps.get_db),
    clientId: str = Query(..., alias="client"),
    userId: str = Query(..., alias="user"),
    templateName: str = Form(..., alias="name"),
    content: str = Form(...),
) -> Any:
    """
    Create new study_template or update study_template.
    """
    study_template, created = await crud.study_template.get_or_create_with_owner_name(
        db=db, ownerSource=clientId, ownerId=userId, name=templateName, content=json.loads(content)
    )

    if not created:
        study_template = await crud.study_template.update(
            db=db,
            db_obj=study_template,
            obj_in=schemas.StudyTemplateUpdate(content=json.loads(content)),
        )
    return schemas.SuccessfulStudyTemplateUpdateDeleteResponse(status=Status.ok)


@router.get(
    "/",
    response_model=SuccessfulResponse[
        Union[List[schemas.StudyTemplateGetList], schemas.StudyTemplateGet]
    ],
)
async def read_study_templates(
    *,
    db: AsyncSession = Depends(deps.get_db),
    clientId: str = Query(..., alias="client"),
    userId: str = Query(..., alias="user"),
    templateName: Optional[str] = Query("", alias="template"),
) -> Any:
    """
    Retrieve study_templates.
    """

    if templateName == "" or templateName is None:
        # Get list
        study_templates = await crud.study_template.get_multi_by_owner(
            db=db, ownerSource=clientId, ownerId=userId
        )
        return SuccessfulResponse(  # type: ignore
            data=[
                schemas.StudyTemplateGetList(name=study_template.name)
                for study_template in study_templates  # type: ignore
            ],
            status=Status.ok,
        )
    study_template = await crud.study_template.get_by_owner_name(
        db=db, ownerSource=clientId, ownerId=userId, name=templateName
    )
    if not study_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study template not found"
        )
    return schemas.StudyTemplateGet(
        name=study_template.name,
        content=study_template.content,  # type: ignore
    )


@router.delete("/", response_model=schemas.SuccessfulStudyTemplateUpdateDeleteResponse)
async def delete_study_template(
    *,
    db: AsyncSession = Depends(deps.get_db),
    clientId: str = Query(..., alias="client"),
    userId: str = Query(..., alias="user"),
    templateName: str = Query(..., alias="template"),
) -> Any:
    """
    Delete an study_template.
    """
    # TODO: Two time query
    study_template = await crud.study_template.get_by_owner_name(
        db=db, ownerSource=clientId, ownerId=userId, name=templateName
    )
    if not study_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Study template not found"
        )
    study_template = await crud.study_template.remove(db=db, id=study_template.id)
    return schemas.SuccessfulStudyTemplateUpdateDeleteResponse(status=Status.ok)
