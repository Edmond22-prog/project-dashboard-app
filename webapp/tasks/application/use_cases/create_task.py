from typing import Optional, Union

from webapp.shared import exceptions
from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    ProjectRepositoryInterface,
    TaskRepositoryInterface,
)


class CreateTaskUseCase:
    """Use case for creating a new task"""

    def __init__(
        self,
        task_repository: Union[BaseRepository, TaskRepositoryInterface],
        project_repository: Union[BaseRepository, ProjectRepositoryInterface],
    ):
        self.task_repository = task_repository
        self.project_repository = project_repository

    def execute(
        self,
        user_id: str,
        project_id: str,
        title: str,
        description: Optional[str] = None,
        status: Optional[str] = None,
        estimated_time: Optional[int] = None,
    ):
        """Execute task creation"""

        existing_project = self.project_repository.get_by_id(project_id)
        if not existing_project:
            raise exceptions.ProjectNotFoundException("Project not found")

        if not self.project_repository.is_owned_by(existing_project, user_id):
            raise exceptions.UnauthorizedAccessException(
                "You are not authorized to create a task on this project"
            )

        # Create task
        task_data = {
            "title": title.strip(),
            "description": description or "",
            "project": existing_project,
        }
        if status:
            task_data["status"] = status

        if estimated_time:
            task_data["estimated_time"] = estimated_time

        task = self.task_repository.create(task_data)
        return task
