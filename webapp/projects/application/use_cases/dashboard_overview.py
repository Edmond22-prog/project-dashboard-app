from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    ProjectRepositoryInterface,
    TaskRepositoryInterface,
)


class DashboardOverviewUseCase:
    """Use case for analytics and dashboard overview"""

    def __init__(
        self,
        project_repository: ProjectRepositoryInterface,
        task_repository: TaskRepositoryInterface,
        user_repository: BaseRepository,
    ):
        self.project_repository = project_repository
        self.task_repository = task_repository
        self.user_repository = user_repository

    def execute(self, user_id: str):
        """Execute to get comprehensive dashboard overview"""

        current_user = self.user_repository.get_by_id(user_id)
        if not current_user:
            Exception("User not found")

        tasks_status_count = self.task_repository.get_tasks_by_status_count(current_user)
        tasks_by_status = {"todo": 0, "in_progress": 0, "done": 0}
        for item in tasks_status_count:
            tasks_by_status[item["status"]] += item["count"]

        tasks_by_time_summary = self.task_repository.get_tasks_time_summary(current_user)
        projects_time_spent = self.project_repository.get_with_time_spent(current_user)
        total_projects = len(self.project_repository.get_by_owner(current_user))
        total_tasks = len(self.task_repository.get_by_user(current_user))

        return {
            "tasks_by_status": tasks_by_status,
            "time_summary": {
                "total_estimated_hours": self._duration_to_hours(
                    tasks_by_time_summary["total_estimated"]
                ),
                "total_spent_hours": self._duration_to_hours(
                    tasks_by_time_summary["total_spent"]
                ),
                "estimated_vs_spent_ratio": self._calculate_time_ratio(
                    tasks_by_time_summary["total_spent"],
                    tasks_by_time_summary["total_estimated"],
                ),
            },
            "projects_time": [
                {
                    "project_id": project["id"],
                    "project_title": project["title"],
                    "time_spent_hours": self._duration_to_hours(
                        project["total_time_spent"]
                    ),
                }
                for project in projects_time_spent
            ],
            "total_projects": total_projects,
            "total_tasks": total_tasks,
        }

    def _duration_to_hours(self, duration):
        """Convert timedelta to hours (float)"""
        if not duration:
            return 0.0

        return round(duration / 60, 2)

    def _calculate_time_ratio(self, spent, estimated):
        """Calculate spent/estimated ratio as percentage"""
        if not estimated or estimated == 0:
            return 0.0

        if not spent:
            return 0.0

        return round((spent / estimated) * 100, 1)
