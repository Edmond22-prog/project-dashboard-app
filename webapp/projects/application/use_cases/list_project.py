from datetime import datetime
from typing import Any, Optional, Union

from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    ProjectRepositoryInterface,
    UserRepositoryInterface,
)


class ListProjectUseCase:
    """Use case for listing user's projects"""

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
        page: int,
        size: int,
        query: Optional[str] = "",
        status: Optional[str] = "",
        start_date: Optional[Any] = None,
        end_date: Optional[Any] = None,
    ):
        """Execute project listing with optional filters and pagination"""

        existing_user = self.user_repository.get_by_id(owner_id)
        if not existing_user:
            raise Exception("User not found")

        parsed_start_date, parsed_end_date = self._parse_and_validate_dates(
            start_date, end_date
        )

        # Building filters
        filters = {}
        if query:
            filters["search_term"] = query

        if status:
            filters["status"] = status

        if parsed_start_date:
            filters["start_date"] = parsed_start_date

        if parsed_end_date:
            filters["end_date"] = parsed_end_date

        searched_projects = self.project_repository.get_by_owner(existing_user, filters)

        # Manage pagination
        start = (page - 1) * size
        end = page * size
        total = len(searched_projects)

        return {
            "page": page,
            "size": size,
            "total": total,
            "more": end < total,
            "projects": searched_projects[start:end] if searched_projects else [],
        }

    @staticmethod
    def _parse_and_validate_dates(
        start_date: Optional[Any] = None, end_date: Optional[Any] = None
    ):
        """Parse and validate date parameters"""

        parsed_start_date = None
        parsed_end_date = None

        if start_date:
            if isinstance(start_date, str):
                try:
                    parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                    parsed_start_date = datetime.combine(
                        parsed_start_date, datetime.min.time()
                    )

                except ValueError:
                    raise ValueError("Invalid format of start_date. Use YYYY-MM-DD")

            else:
                parsed_start_date = start_date

        if end_date:
            if isinstance(end_date, str):
                try:
                    parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                    parsed_end_date = datetime.combine(
                        parsed_end_date, datetime.max.time()
                    )

                except ValueError:
                    raise ValueError("Invalid format of end_date. Use YYYY-MM-DD")

            else:
                parsed_end_date = end_date

        if parsed_start_date and parsed_end_date and parsed_start_date > parsed_end_date:
            raise ValueError("start_date must be lower or equal to end_date")

        return parsed_start_date, parsed_end_date
