from typing import Union

from webapp.shared import exceptions
from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    UserRepositoryInterface,
)
from webapp.users.application.services.jwt_service import JWTAuthService


class AuthenticateUserUseCase:
    """Use case for user authentication"""

    def __init__(
        self,
        user_repository: Union[BaseRepository, UserRepositoryInterface],
        auth_service: JWTAuthService,
    ):
        self.user_repository = user_repository
        self.auth_service = auth_service

    def execute(self, username, password):
        """Execute user authentication"""

        if not self.user_repository.check_password(username=username, password=password):
            raise exceptions.ValidationException("Invalid credentials")

        existing_user = self.user_repository.get_by_username(username)
        # Generate tokens
        tokens = self.auth_service.generate_tokens(existing_user)

        return tokens
