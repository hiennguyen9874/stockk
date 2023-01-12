from celery import current_app as current_celery_app

from app.core.settings import settings

print(
    "CELERY_BROKER_URL:",
    settings.CELERY_BROKER_URL,
)
print(
    "CELERY_RESULT_BACKEND:",
    settings.CELERY_RESULT_BACKEND,
)
print(
    "CELERY_RESULT_SERIALIZER:",
    settings.CELERY_RESULT_SERIALIZER,
)
print(
    "CELERY_TASK_SERIALIZER:",
    settings.CELERY_TASK_SERIALIZER,
)
print(
    "CELERY_ACCEPT_CONTENT:",
    settings.CELERY_ACCEPT_CONTENT,
)
print(
    "CELERY_ENABLE_UTC:",
    settings.CELERY_ENABLE_UTC,
)
print(
    "CELERY_TIMEZONE:",
    settings.CELERY_TIMEZONE,
)
print(
    "CELERY_IMPORTS:",
    settings.CELERY_IMPORTS,
)
print(
    "CELERY_BEAT_SCHEDULE:",
    settings.CELERY_BEAT_SCHEDULE,
)


def create_celery_app():
    celery_app = current_celery_app
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
