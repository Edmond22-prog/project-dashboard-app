from django.db import models

from utils.common import generate_uuid


class BaseModel(models.Model):
    """Base model with common fields"""

    id = models.CharField(
        max_length=100, primary_key=True, default=generate_uuid, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
