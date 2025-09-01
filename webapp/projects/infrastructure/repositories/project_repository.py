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

    def get_by_owner(self, user, filters_dict=None):
        """Get all projects owned by user with filters"""
        q = Q(owner=user)
        distinct = False
        if filters_dict:
            if filters_dict.get("search_term", ""):
                q &= Q(title__icontains=filters_dict["search_term"]) | Q(
                    description__icontains=filters_dict["search_term"]
                )

            if filters_dict.get("status", ""):
                distinct = True
                q &= Q(tasks__status=filters_dict["status"])

            if filters_dict.get("start_date", ""):
                q &= Q(created_at__gte=filters_dict["start_date"])

            if filters_dict.get("end_date", ""):
                q &= Q(created_at__lte=filters_dict["end_date"])

        projects = Project.objects.filter(q).select_related("owner")
        if distinct:
            projects = projects.distinct()

        return projects.order_by("-created_at").annotate(
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

    def is_owned_by(self, project, user_id):
        """Check if the user is owner of a project"""
        if project.owner.id == user_id:
            return True

        return False
