from datetime import timedelta

from django.db import models

from app_models.models.base_model import BaseModel
from app_models.models.constant import TASK_STATUS_CHOICES, TaskStatus
from app_models.models.project import Project


class Task(BaseModel):
    """Task model - belongs to a project"""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=TASK_STATUS_CHOICES, default=TaskStatus.TODO
    )
    estimated_time = models.DurationField(
        null=True, blank=True, help_text="Estimated time in HH:MM format"
    )
    spent_time = models.DurationField(
        default=timedelta(0), help_text="Total time spent on this task"
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return f"{self.title} ({self.status})"
