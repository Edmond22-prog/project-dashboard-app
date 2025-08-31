from rest_framework import serializers

from app_models.models.project import Project


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"
    
    def get_owner(self, obj):
        return obj.owner.username

