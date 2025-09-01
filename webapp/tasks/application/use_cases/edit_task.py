from typing import Optional, Union

from webapp.shared import exceptions
from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    TaskRepositoryInterface,
)


class EditTaskUseCase:
    """Use case for editing a task"""

    def __init__(
        self,
        user_repository: Union[BaseRepository],
        task_repository: Union[BaseRepository, TaskRepositoryInterface],
    ):
        self.user_repository = user_repository
        self.task_repository = task_repository

    def execute(
        self,
        user_id: str,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        estimated_time: Optional[int] = None,
    ):
        """Execute task editing"""

        existing_user = self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise Exception("User not found")

        existing_task = self.task_repository.get_by_id(task_id)
        if not existing_user:
            raise exceptions.TaskNotFoundException("Task not found")

        if existing_task.project.owner != existing_user:
            raise exceptions.UnauthorizedAccessException(
                "You are not authorized to edit this task"
            )

        # Update project data
        task_data = {}
        if title is not None:
            task_data["title"] = title

        if description is not None:
            task_data["description"] = description

        if status is not None:
            task_data["status"] = status

        if estimated_time is not None:
            task_data["estimated_time"] = estimated_time

        if task_data:
            return self.task_repository.update(existing_task, task_data)

        return existing_task
