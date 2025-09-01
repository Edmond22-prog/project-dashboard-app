from rest_framework import serializers

from app_models.models.task import Task


class CreateTaskSerializer(serializers.ModelSerializer):
    project_id = serializers.CharField()

    class Meta:
        model = Task
        fields = ("title", "description", "status", "estimated_time", "project_id")
