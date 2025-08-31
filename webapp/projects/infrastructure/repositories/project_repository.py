from django.db.models import Count, Prefetch, Q, Sum

from app_models.models.constant import TaskStatus
from app_models.models.project import Project
from app_models.models.task import Task
from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    ProjectRepositoryInterface,
)


class ProjectRepository(BaseRepository, ProjectRepositoryInterface):
    """Repository for Project entity operations"""

    def get_by_id(self, id):
        """Get project by ID"""
        try:
            return Project.objects.select_related("owner").get(id=id)

        except Project.DoesNotExist:
            return None

    def get_by_owner(self, user):
        """Get all projects owned by user"""
        return (
            Project.objects.filter(owner=user)
            .select_related("owner")
            .order_by("-created_at")
        )

    def get_with_task_statistics(self, user):
        """Get projects with task statistics"""
        return self.get_by_owner(user).annotate(
            total_tasks=Count("tasks"),
            completed_tasks=Count("tasks", filter=Q(tasks__status=TaskStatus.DONE)),
            total_estimated_time=Sum("tasks__estimated_time"),
            total_spent_time=Sum("tasks__spent_time"),
        )

    def get_with_tasks(self, project_id, user):
        """Get project with its tasks"""
        try:
            return (
                Project.objects.select_related("owner")
                .prefetch_related(
                    Prefetch(
                        "tasks",
                        queryset=Task.objects.select_related("project").order_by(
                            "-created_at"
                        ),
                    )
                )
                .get(id=project_id, owner=user)
            )

        except Project.DoesNotExist:
            return None

    def create(self, project_data):
        """Create new project"""
        project = Project.objects.create(**project_data)
        return project

    def update(self, project, data):
        """Update project data"""
        for field, value in data.items():
            if hasattr(project, field) and field != "owner":
                setattr(project, field, value)

        project.save()
        return project

    def delete(self, project):
        """Delete project"""
        project.delete()
        return True

    def search(self, user, search_term):
        """Search projects by title or description"""
        return self.get_by_owner(user).filter(
            Q(title__icontains=search_term) | Q(description__icontains=search_term)
        )

    def filter_by_task_status(self, user, status):
        """Filter projects that have tasks with specific status"""
        return self.get_by_owner(user).filter(tasks__status=status).distinct()

    def filter_by_date_range(self, user, start_date, end_date):
        """Filter projects by creation date range"""
        queryset = self.get_by_owner(user)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)

        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        return queryset
