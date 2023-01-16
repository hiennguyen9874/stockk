from typing import Any

from fastapi import APIRouter, Depends

from app import models, schemas
from app.api import deps
from app.schemas.response import Status, SuccessfulResponse
from app.tasks import test_celery as test_celery_task, task_crawl_ticker

router = APIRouter()


@router.post("/test-celery", response_model=SuccessfulResponse[schemas.Msg], status_code=201)
async def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Test Celery worker.
    """
    # task = test_celery_task.delay(msg.msg)
    task = task_crawl_ticker.delay()
    task.get()
    return SuccessfulResponse(data={"msg": "Word received"}, status=Status.ok)


# Calling this endpoint to see if the setup works. If yes, an error message will show in Sentry dashboard
@router.get("/test-sentry")
async def test_sentry() -> None:  # sourcery skip: raise-specific-error
    """
    Test Sentry.
    """
    raise Exception("Test sentry integration")
