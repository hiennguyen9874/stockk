from celery import Celery

from app.core.settings import settings


def create_celery_app() -> Celery:
    celery_app = Celery("worker", broker=settings.CELERY_BROKER_URL)
    celery_app.conf.update(
        broker_url=settings.CELERY_BROKER_URL,
        result_backend=settings.CELERY_RESULT_BACKEND,
        result_serializer=settings.CELERY_RESULT_SERIALIZER,
        task_serializer=settings.CELERY_TASK_SERIALIZER,
        accept_content=settings.CELERY_ACCEPT_CONTENT,
        enable_utc=settings.CELERY_ENABLE_UTC,
        timezone=settings.CELERY_TIMEZONE,
        imports=settings.CELERY_IMPORTS,
        beat_schedule=settings.CELERY_BEAT_SCHEDULE,
    )
    celery_app.autodiscover_tasks(["app"])
    return celery_app
