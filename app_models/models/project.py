from django.contrib.auth.models import User
from django.db import models

from app_models.models.base_model import BaseModel


class Project(BaseModel):
    """Project model - contains multiple tasks"""

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_projects"
    )

    def __str__(self):
        return self.title
