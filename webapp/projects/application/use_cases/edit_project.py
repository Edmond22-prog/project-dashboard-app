from typing import Optional, Union

from webapp.shared import exceptions
from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    ProjectRepositoryInterface,
    UserRepositoryInterface,
)


class EditProjectUseCase:
    """Use case for editing a project"""

    def __init__(
        self,
        project_repository: Union[BaseRepository, ProjectRepositoryInterface],
        user_repository: Union[BaseRepository, UserRepositoryInterface],
    ):
        self.project_repository = project_repository
        self.user_repository = user_repository

    def execute(
        self,
        owner_id: str,
        project_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ):
        """Execute project editing"""

        existing_user = self.user_repository.get_by_id(owner_id)
        if not existing_user:
            raise Exception("User not found")

        existing_project = self.project_repository.get_by_id(project_id)
        if not existing_project:
            raise exceptions.ProjectNotFoundException("Project not found")

        if existing_project.owner != existing_user:
            raise exceptions.UnauthorizedAccessException(
                "You are not authorized to edit this project"
            )

        # Update project data
        project_data = {}
        if title is not None:
            project_data["title"] = title

        if description is not None:
            project_data["description"] = description

        if project_data:
            return self.project_repository.update(existing_project, project_data)

        return existing_project
