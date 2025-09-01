from django.db.models import Count, F, Prefetch, Q

from app_models.models.task import Task
from app_models.models.time_entry import TimeEntry
from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    TaskRepositoryInterface,
)


class TaskRepository(BaseRepository, TaskRepositoryInterface):
    """Repository for Task entity operations"""

    def get_by_id(self, task_id):
        """Get task by ID with related data"""
        try:
            return Task.objects.select_related("project", "project__owner").get(
                id=task_id
            )

        except Task.DoesNotExist:
            return None

    def get_by_project(self, project):
        """Get all tasks for a project"""
        return (
            Task.objects.filter(project=project)
            .select_related("project")
            .order_by("-created_at")
        )

    def get_by_user(self, user, filters=None):
        """Get all tasks accessible by user with optional filters"""
        q = Q(project__owner=user)
        if filters:
            if filters.get("search_term", ""):
                q &= Q(title__icontains=filters["search_term"]) | Q(
                    description__icontains=filters["search_term"]
                )

            if filters.get("status", ""):
                q &= Q(status=filters["status"])

            if filters.get("project", ""):
                q &= Q(project=filters["project"])

        return (
            Task.objects.filter(q)
            .select_related("project", "project__owner")
            .order_by("-created_at")
        )

    def get_with_active_timer(self, user):
        """Get tasks with active timer information"""
        return self.get_by_user(user).prefetch_related(
            Prefetch(
                "time_entries",
                queryset=TimeEntry.objects.filter(is_active=True),
                to_attr="active_timers",
            )
        )

    def create(self, task_data):
        """Create new task"""
        task = Task.objects.create(**task_data)
        return task

    def update(self, task, data):
        """Update task data"""
        for field, value in data.items():
            if hasattr(task, field) and field not in ["project", "spent_time"]:
                setattr(task, field, value)

        task.save()
        return task

    def delete(self, task):
        """Delete task"""
        task.delete()
        return True

    def get_overdue_tasks(self, user):
        """Get tasks that are overdue (spent more than estimated)"""
        return self.get_by_user(user).filter(
            estimated_time__isnull=False, spent_time__gt=F("estimated_time")
        )

    def get_tasks_by_status_count(self, user):
        """Get task count by status for dashboard"""
        return self.get_by_user(user).values("status").annotate(count=Count("id"))

    def update_spent_time(self, task, duration):
        """Update task spent time by adding duration"""
        task.spent_time += duration
        task.save(update_fields=["spent_time"])
        return task
