from django.contrib.auth.models import User
from django.db import models

from app_models.models.base_model import BaseModel
from app_models.models.task import Task


class TimeEntry(BaseModel):
    """Time tracking entries for tasks"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="time_entries")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="time_entries")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time and not self.duration:
            self.duration = (self.end_time - self.start_time).seconds // 60

        super().save(*args, **kwargs)
    
    def __str__(self):
        status = "Active" if self.is_active else "Completed"
        return f"{self.task.title} - {status} ({self.user.username})"
