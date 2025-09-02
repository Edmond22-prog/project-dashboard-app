from datetime import datetime
from typing import Union

from webapp.shared import exceptions
from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    TimeEntryRepositoryInterface,
)


class StartTimerUseCase:
    """Use case for starting a timer on a task"""

    def __init__(
        self,
        task_repository: BaseRepository,
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

        # Check if task already has active timer
        if self.time_entry_repository.has_active_timer(existing_task):
            raise exceptions.ActiveTimerExistsException(
                "Task already has an active timer"
            )

        # Stop any other active timers for this user
        self.time_entry_repository.stop_active_timers_for_user(existing_user)

        # Create new timer
        timer_data = {
            "user": existing_user,
            "task": existing_task,
            "start_time": datetime.now(),
            "is_active": True,
        }

        timer = self.time_entry_repository.create(timer_data)
        return timer
