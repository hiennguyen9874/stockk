import os

from app.worker import app

__all__ = ["task_delete_file"]


@app.task(name="task_delete_file")
def task_delete_file(file_path: str) -> None:
    if os.path.exists(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
