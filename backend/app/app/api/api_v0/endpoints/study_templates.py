from typing import Any, Optional, Dict, Union, List

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.schemas.response import Status, SuccessfulResponse

router = APIRouter()


@router.post("/", response_model=schemas.SuccessfulStudyTemplateUpdateDeleteResponse)
async def create_update_study_template(
    *,
    db: AsyncSession = Depends(deps.get_db),
    clientId: str = Query(..., alias="client"),
    userId: str = Query(..., alias="user"),
    templateName: str = Body(..., alias="name"),
    content: Dict[Any, Any] = Body(...),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new study_template or update study_template.
    """
    study_template, created = crud.study_template.get_or_create_with_owner_name(
        db=db, ownerSource=clientId, ownerId=userId, name=templateName, content=content
    )

    if not created:
        study_template = await crud.study_template.update(
            db=db,
            db_obj=study_template,
            obj_in=schemas.StudyTemplateUpdate(content=content),
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
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve study_templates.
    """

    if templateName == "" or templateName is None:
        # Get list
        study_templates = await crud.study_template.get_multi_by_owner(
            db=db, ownerSource=clientId, ownerId=userId
        )
        return SuccessfulResponse(
            data=[
                schemas.StudyTemplateGetList(name=study_template.name)
                for study_template in study_templates
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
        content=study_template.content,
    )


@router.delete("/", response_model=schemas.SuccessfulStudyTemplateUpdateDeleteResponse)
async def delete_study_template(
    *,
    db: AsyncSession = Depends(deps.get_db),
    clientId: str = Query(..., alias="client"),
    userId: str = Query(..., alias="user"),
    templateName: str = Query(..., alias="template"),
    current_user: models.User = Depends(deps.get_current_active_user),
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
