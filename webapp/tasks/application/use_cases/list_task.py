from typing import Optional, Union

from webapp.shared import exceptions
from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    ProjectRepositoryInterface,
    TaskRepositoryInterface,
)


class ListTasksUseCase:
    """Use case for listing user's tasks"""

    def __init__(
        self,
        project_repository: Union[BaseRepository, ProjectRepositoryInterface],
        user_repository: Union[BaseRepository],
        task_repository: Union[TaskRepositoryInterface],
    ):
        self.project_repository = project_repository
        self.user_repository = user_repository
        self.task_repository = task_repository

    def execute(
        self,
        user_id: str,
        page: int,
        size: int,
        query: Optional[str] = "",
        status: Optional[str] = "",
        project_id: Optional[str] = None,
    ):
        """Execute tasks listing with optional filters and pagination"""

        existing_user = self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise Exception("User not found")

        # Building filters
        filters = {}
        if query:
            filters["search_term"] = query

        if status:
            filters["status"] = status

        if project_id:
            existing_project = self.project_repository.get_by_id(project_id)
            if not existing_project:
                raise exceptions.ProjectNotFoundException("Project not found")

            if not self.project_repository.is_owned_by(existing_project, user_id):
                raise exceptions.UnauthorizedAccessException(
                    "You are not authorized to access on this project"
                )

            filters["project"] = existing_project

        searched_tasks = self.task_repository.get_by_user(existing_user, filters)

        # Manage pagination
        start = (page - 1) * size
        end = page * size
        total = len(searched_tasks)

        return {
            "page": page,
            "size": size,
            "total": total,
            "more": end < total,
            "projects": searched_tasks[start:end] if searched_tasks else [],
        }
