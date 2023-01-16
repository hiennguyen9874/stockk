import json
from typing import Any, Optional, Dict, Union, List

from fastapi import APIRouter, Depends, HTTPException, status, Query, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.api import deps
from app.schemas.response import Status, SuccessfulResponse

router = APIRouter()


@router.post("/", response_model=schemas.SuccessfulDrawingTemplateUpdateDeleteResponse)
async def create_update_drawing_template(
    *,
    db: AsyncSession = Depends(deps.get_db),
    clientId: str = Query(..., alias="client"),
    userId: str = Query(..., alias="user"),
    name: str = Query(...),
    tool: str = Query(...),
    content: str = Form(...),
) -> Any:
    """
    Create new drawing_template or update drawing_template.
    """
    drawing_template, created = await crud.drawing_template.get_or_create_with_owner_name(
        db=db, ownerSource=clientId, ownerId=userId, name=name, content=json.loads(content)
    )
    if not created:
        drawing_template = await crud.drawing_template.update(
            db=db,
            db_obj=drawing_template,
            obj_in=schemas.DrawingTemplateUpdate(
                content=json.loads(content),
            ),
        )
    return schemas.SuccessfulDrawingTemplateUpdateDeleteResponse(status=Status.ok)


@router.get("/", response_model=SuccessfulResponse[Union[List[str], schemas.DrawingTemplateGet]])
async def read_drawing_templates(
    *,
    db: AsyncSession = Depends(deps.get_db),
    clientId: str = Query(..., alias="client"),
    userId: str = Query(..., alias="user"),
    tool: str = Query(...),
    name: Optional[str] = Query(""),
) -> Any:
    """
    Retrieve drawing_templates.
    """
    if name == "" or name is None:
        # Get list
        drawing_templates = await crud.drawing_template.get_multi_by_owner_tool(
            db=db, ownerSource=clientId, ownerId=userId, tool=tool
        )
        return SuccessfulResponse(  # type: ignore
            data=[drawing_template.name for drawing_template in drawing_templates],  # type: ignore
            status=Status.ok,
        )
    drawing_template = await crud.drawing_template.get_by_owner_tool_name(
        db=db, ownerSource=clientId, ownerId=userId, name=name, tool=tool
    )
    if not drawing_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Drawing template not found"
        )
    return schemas.DrawingTemplateGet(
        name=drawing_template.name,
        content=drawing_template.content,  # type: ignore
    )


@router.delete("/", response_model=schemas.SuccessfulDrawingTemplateUpdateDeleteResponse)
async def delete_drawing_template(
    *,
    db: AsyncSession = Depends(deps.get_db),
    clientId: str = Query(..., alias="client"),
    userId: str = Query(..., alias="user"),
    tool: str = Query(...),
    name: str = Query(...),
) -> Any:
    """
    Delete an drawing_template.
    """
    # TODO: Two time query
    drawing_template = await crud.drawing_template.get_by_owner_tool_name(
        db=db, ownerSource=clientId, ownerId=userId, tool=tool, name=name
    )
    if not drawing_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Drawing template not found"
        )
    drawing_template = await crud.drawing_template.remove(db=db, id=drawing_template.id)
    return schemas.SuccessfulDrawingTemplateUpdateDeleteResponse(status=Status.ok)
