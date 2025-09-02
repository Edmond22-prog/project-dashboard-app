from datetime import datetime, timezone
from typing import Union

from webapp.shared import exceptions
from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    TaskRepositoryInterface,
    TimeEntryRepositoryInterface,
)


class StopTimerUseCase:
    """Use case for stopping a timer on a task"""

    def __init__(
        self,
        task_repository: Union[BaseRepository, TaskRepositoryInterface],
        time_entry_repository: Union[BaseRepository, TimeEntryRepositoryInterface],
        user_repository: BaseRepository,
    ):
        self.task_repository = task_repository
        self.time_entry_repository = time_entry_repository
        self.user_repository = user_repository

    def execute(self, user_id: str, task_id: str):
        """Execute timer start"""

        existing_task = self.task_repository.get_by_id(task_id)
        if not existing_task:
            raise exceptions.TaskNotFoundException("Task not found")

        existing_user = self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise Exception("User not found")

        if existing_task.project.owner != existing_user:
            raise exceptions.UnauthorizedAccessException(
                "You don't have access to this task"
            )

        existing_active_timer = self.time_entry_repository.get_active_timer_for_task(
            existing_task, existing_user
        )
        if not existing_active_timer:
            raise exceptions.NoActiveTimerException("No active timer found for this task")

        # Stop active time
        end_time = datetime.now(timezone.utc)
        duration = (end_time - existing_active_timer.start_time).seconds // 60
        is_active = False
        _ = self.time_entry_repository.update(
            existing_active_timer,
            {"end_time": end_time, "duration": duration, "is_active": is_active},
        )

        # Update task
        _ = self.task_repository.update_spent_time(existing_task, duration)

        return {"task": existing_task.title, "duration": duration}
