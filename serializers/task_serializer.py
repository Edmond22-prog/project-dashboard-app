from rest_framework import serializers

from app_models.models.task import Task
from app_models.models.time_entry import TimeEntry


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class TaskTimeEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeEntry
        fields = "__all__"
