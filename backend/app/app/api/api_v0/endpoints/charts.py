import time
from typing import Any, Optional, Dict, Union, List

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from fastapi_pagination.api import create_page, resolve_params
from fastapi_pagination.default import Page, Params
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.schemas.response import Status, SuccessfulResponse
from app.utils import get_limit_offset

router = APIRouter()


@router.post(
    "/",
    response_model=Union[
        schemas.SuccessfulChartCreateResponse, schemas.SuccessfulChartUpdateDeleteResponse
    ],
)
async def create_update_chart(
    *,
    db: AsyncSession = Depends(deps.get_db),
    clientId: str = Query(..., alias="client"),
    userId: str = Query(..., alias="user"),
    chartId: Optional[str] = Query(""),
    chartName: str = Body(..., alias="name"),
    symbol: str = Body(...),
    resolution: str = Body(...),
    content: Dict[Any, Any] = Body(...),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new chart or update chart with chartId when charID != ''.
    """
    if chartId == "" or chartId is None:
        chart = await crud.chart.create(
            db=db,
            obj_in=schemas.ChartCreate(
                ownerSource=clientId,
                ownerId=userId,
                name=chartName,
                symbol=symbol,
                resolution=resolution,
                content=content,
            ),
        )
        return schemas.SuccessfulChartCreateResponse(id=chart.id, status=Status.ok)

    chart = await crud.chart.get(db=db, id=int(chartId))
    if not chart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chart not found")
    chart = await crud.chart.update(
        db=db,
        db_obj=chart,
        obj_in=schemas.ChartUpdate(
            ownerSource=clientId,
            ownerId=userId,
            name=chartName,
            symbol=symbol,
            resolution=resolution,
            content=content,
        ),
    )
    return schemas.SuccessfulChartUpdateDeleteResponse(status=Status.ok)


@router.get(
    "/", response_model=SuccessfulResponse[Union[List[schemas.ChartGetList], schemas.ChartGet]]
)
async def read_charts(
    *,
    db: AsyncSession = Depends(deps.get_db),
    clientId: str = Query(..., alias="client"),
    userId: str = Query(..., alias="user"),
    chartId: Optional[str] = Query(""),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve charts.
    """
    # charts, total = await crud.chart.get_multi_count(db, offset=offset, limit=limit)
    # return SuccessfulResponse(data=create_page(charts, total, params), status=Status.ok)

    if chartId == "" or chartId is None:
        # Get list
        charts = await crud.chart.get_multi_by_owner(db=db, ownerSource=clientId, ownerId=userId)
        return SuccessfulResponse(
            data=[
                schemas.ChartGetList(
                    id=chart.id,
                    name=chart.name,
                    symbol=chart.symbol,
                    resolution=chart.resolution,
                    timestamp=time.mktime(chart.lastModified.timetuple()),
                )
                for chart in charts
            ],
            status=Status.ok,
        )
    chart = await crud.chart.get_by_id_owner(
        db=db, id=chartId, ownerSource=clientId, ownerId=userId
    )
    if not chart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chart not found")
    return schemas.ChartGet(
        id=chart.id,
        name=chart.name,
        symbol=chart.symbol,
        resolution=chart.resolution,
        timestamp=time.mktime(chart.lastModified.timetuple()),
        content=chart.content,
    )


@router.delete("/", response_model=SuccessfulResponse[schemas.Chart])
async def delete_chart(
    *,
    db: AsyncSession = Depends(deps.get_db),
    clientId: str = Query(..., alias="client"),
    userId: str = Query(..., alias="user"),
    chartId: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an chart.
    """
    # TODO: Two time query
    chart = await crud.chart.get_by_id_owner(
        db=db, id=chartId, ownerSource=clientId, ownerId=userId
    )
    if not chart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chart not found")
    chart = await crud.chart.remove(db=db, id=chartId)
    return schemas.SuccessfulChartUpdateDeleteResponse(status=Status.ok)
