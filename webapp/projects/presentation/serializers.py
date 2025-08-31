from rest_framework import serializers

from app_models.models.project import Project


class CreateProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ["title", "description"]
