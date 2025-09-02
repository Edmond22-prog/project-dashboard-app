from django.db.models import Sum
from django.utils import timezone

from app_models.models.time_entry import TimeEntry
from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    TimeEntryRepositoryInterface,
)


class TimeEntryRepository(BaseRepository, TimeEntryRepositoryInterface):
    """Repository for TimeEntry entity operations"""

    def get_by_id(self, entry_id):
        """Get time entry by ID"""
        try:
            return TimeEntry.objects.select_related("user", "task", "task__project").get(
                id=entry_id
            )

        except TimeEntry.DoesNotExist:
            return None

    def get_by_task(self, task):
        """Get all time entries for a task"""
        return (
            TimeEntry.objects.filter(task=task)
            .select_related("user", "task")
            .order_by("-start_time")
        )

    def get_by_user(self, user):
        """Get all time entries for a user"""
        return (
            TimeEntry.objects.filter(task__project__owner=user)
            .select_related("user", "task", "task__project")
            .order_by("-start_time")
        )

    def get_by_user_and_date(self, user, date):
        """Get time entries for user on specific date"""
        return TimeEntry.objects.filter(
            task__project__owner=user, start_time__date=date
        ).select_related("task", "task__project")

    def get_active_timer_for_user(self, user):
        """Get active timer for user"""
        return (
            TimeEntry.objects.filter(task__project__owner=user, is_active=True)
            .select_related("task", "task__project")
            .first()
        )

    def get_active_timer_for_task(self, task, user=None):
        """Get active timer for a specific task"""
        filters = {"task": task, "is_active": True}
        if user:
            filters["user"] = user

        return TimeEntry.objects.filter(**filters).first()

    def has_active_timer(self, task):
        """Check if task has an active timer"""
        return TimeEntry.objects.filter(task=task, is_active=True).exists()

    def create(self, entry_data):
        """Create new time entry"""
        entry = TimeEntry.objects.create(**entry_data)
        return entry

    def update(self, entry, data):
        """Update time entry data"""
        for field, value in data.items():
            if hasattr(entry, field):
                setattr(entry, field, value)

        entry.save()
        return entry

    def delete(self, entry):
        """Delete time entry"""
        entry.delete()
        return True

    def stop_active_timers_for_user(self, user):
        """Stop all active timers for a user"""
        active_timers = TimeEntry.objects.filter(
            task__project__owner=user, is_active=True
        )

        current_time = timezone.now()
        for timer in active_timers:
            timer.end_time = current_time
            timer.duration = (current_time - timer.start_time).seconds // 60
            timer.is_active = False
            timer.save()

            # Update task spent time
            timer.task.spent_time += timer.duration
            timer.task.save(update_fields=["spent_time"])

        return active_timers.count()

    def get_time_summary_for_project(self, project):
        """Get time summary for a project"""
        entries = self.get_by_task_project(project).filter(duration__isnull=False)

        total_time = entries.aggregate(total=Sum("duration"))["total"]
        entry_count = entries.count()

        return {
            "total_time": total_time or 0,
            "entry_count": entry_count,
        }

    def get_by_task_project(self, project):
        """Get time entries for all tasks in a project"""
        return TimeEntry.objects.filter(task__project=project).select_related(
            "user", "task"
        )

    def get_weekly_summary(self, user, week_start):
        """Get weekly time tracking summary"""
        week_end = week_start + timezone.timedelta(days=7)

        entries = TimeEntry.objects.filter(
            task__project__owner=user,
            start_time__gte=week_start,
            start_time__lt=week_end,
            duration__isnull=False,
        ).select_related("task", "task__project")

        total_time = entries.aggregate(total=Sum("duration"))["total"]

        # Group by day
        daily_summary = {}
        for entry in entries:
            day = entry.start_time.date()
            if day not in daily_summary:
                daily_summary[day] = {"entries": [], "total_time": 0}

            daily_summary[day]["entries"].append(entry)
            daily_summary[day]["total_time"] += entry.duration

        return {
            "week_start": week_start,
            "week_end": week_end,
            "total_time": total_time or 0,
            "daily_summary": daily_summary,
        }
