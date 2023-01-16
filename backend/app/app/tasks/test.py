from app.worker import app

__all__ = ["test_celery", "task_schedule_work"]


@app.task(name="test_celery")
def test_celery(word: str) -> str:
    return f"test task return {word}"


@app.task(name="task_schedule_work")
def task_schedule_work() -> None:
    print("task_schedule_work run")
