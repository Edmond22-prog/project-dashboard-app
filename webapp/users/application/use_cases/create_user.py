from typing import Optional, Union

from webapp.shared import exceptions
from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    UserRepositoryInterface,
)


class CreateUserUseCase:
    """Use case for creating a new user"""

    def __init__(self, user_repository: Union[BaseRepository, UserRepositoryInterface]):
        self.user_repository = user_repository

    def execute(
        self,
        username: str,
        email: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ):
        """Execute user creation"""

        # Check if user already exists
        if self.user_repository.exists_by_username(username):
            raise exceptions.ValidationException("Username already exists !")

        if self.user_repository.exists_by_email(email):
            raise exceptions.ValidationException("Email already exists !")

        # Create user
        user_data = {
            "username": username,
            "email": email,
            "first_name": first_name or "",
            "last_name": last_name or "",
            "password": password,
        }

        user = self.user_repository.create(user_data)
        return user
