from rest_framework import serializers

from app_models.models.project import Project


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    def get_owner(self, obj):
        return obj.owner.username


class ProjectsWithTaskStatistics(ProjectSerializer):
    total_tasks = serializers.SerializerMethodField()
    completed_tasks = serializers.SerializerMethodField()
    total_estimated_time = serializers.SerializerMethodField()
    total_spent_time = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    def get_total_tasks(self, obj):
        return obj.total_tasks

    def get_completed_tasks(self, obj):
        return obj.completed_tasks

    def get_total_estimated_time(self, obj):
        return obj.total_estimated_time

    def get_total_spent_time(self, obj):
        return obj.total_spent_time
