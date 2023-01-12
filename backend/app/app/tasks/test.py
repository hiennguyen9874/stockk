from celery import shared_task

__all__ = ["test_celery", "task_schedule_work"]


@shared_task(name="test_celery")
def test_celery(word: str) -> str:
    return f"test task return {word}"


@shared_task(name="task_schedule_work")
def task_schedule_work() -> None:
    print("task_schedule_work run")
