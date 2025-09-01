import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from middlewares.auth_middleware import check_user_is_connected
from serializers import TaskSerializer
from utils.user_utils import get_connected_user
from webapp.projects.infrastructure.repositories import ProjectRepository
from webapp.tasks.application.use_cases import CreateTaskUseCase
from webapp.tasks.infrastructure.repositories import TaskRepository
from webapp.tasks.presentation.serializers import CreateTaskSerializer


class CreateTaskAPIView(APIView):
    serializer_class = CreateTaskSerializer

    @swagger_auto_schema(
        operation_id="create_task",
        operation_description="Endpoint for the creation of a task",
        operation_summary="Create a task",
        request_body=CreateTaskSerializer(),
        responses={
            201: TaskSerializer(),
            400: '{"error": "Invalid data provided for task creation"}',
            404: '{"error": "You are not connected !"}',
            500: '{"error": "Task creation failed"}',
        },
        tags=["Tasks"],
        security=[{"Bearer": []}],
    )
    @check_user_is_connected
    def post(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        if not serialized.is_valid():
            logging.exception(serialized.errors)
            return Response(
                {"error": "Invalid data provided for task creation"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        connected_user = get_connected_user(request)
        validated_data = serialized.validated_data
        use_case = CreateTaskUseCase(TaskRepository(), ProjectRepository())

        try:
            created_task = use_case.execute(
                user_id=connected_user.id,
                project_id=validated_data["project_id"],
                title=validated_data["title"],
                description=validated_data.get("description"),
                status=validated_data.get("status"),
                estimated_time=validated_data.get("estimated_time"),
            )

            return Response(
                TaskSerializer(created_task).data, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logging.exception(f"Error during project creation: {e}")
            return Response(
                {"error": "Project creation failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
