from typing import Optional, Union

from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    ProjectRepositoryInterface,
    UserRepositoryInterface,
)


class CreateProjectUseCase:
    """Use case for creating a new project"""

    def __init__(
        self,
        project_repository: Union[BaseRepository, ProjectRepositoryInterface],
        user_repository: Union[BaseRepository, UserRepositoryInterface],
    ):
        self.project_repository = project_repository
        self.user_repository = user_repository

    def execute(self, owner_id: str, title: str, description: Optional[str] = None):
        """Execute project creation"""

        existing_user = self.user_repository.get_by_id(owner_id)
        if not existing_user:
            raise Exception("User not found")

        # Create project
        project_data = {
            "title": title.strip(),
            "description": description or "",
            "owner": existing_user,
        }

        project = self.project_repository.create(project_data)
        return project
