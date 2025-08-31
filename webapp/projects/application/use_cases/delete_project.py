from typing import Union

from webapp.shared import exceptions
from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    ProjectRepositoryInterface,
    UserRepositoryInterface,
)


class DeleteProjectUseCase:
    """Use case for deleting a project"""

    def __init__(
        self,
        project_repository: Union[BaseRepository, ProjectRepositoryInterface],
        user_repository: Union[BaseRepository, UserRepositoryInterface],
    ):
        self.project_repository = project_repository
        self.user_repository = user_repository

    def execute(self, owner_id: str, project_id: str):
        """Execute project deleting"""

        existing_user = self.user_repository.get_by_id(owner_id)
        if not existing_user:
            raise Exception("User not found")

        existing_project = self.project_repository.get_by_id(project_id)
        if not existing_project:
            raise exceptions.ProjectNotFoundException("Project not found")

        if existing_project.owner != existing_user:
            raise exceptions.UnauthorizedAccessException(
                "You are not authorized to delete this project"
            )

        return self.project_repository.delete(existing_project)
