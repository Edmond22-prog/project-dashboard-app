import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from middlewares.auth_middleware import check_user_is_connected
from serializers import ProjectSerializer
from utils.user_utils import get_connected_user
from webapp.projects.application.use_cases import (
    CreateProjectUseCase,
    DeleteProjectUseCase,
    EditProjectUseCase,
)
from webapp.projects.infrastructure.repositories import ProjectRepository
from webapp.projects.presentation.serializers import (
    CreateProjectSerializer,
    EditProjectSerializer,
)
from webapp.users.infrastructure.repositories import UserRepository


class CreateProjectAPIView(APIView):
    serializer_class = CreateProjectSerializer

    @swagger_auto_schema(
        operation_id="create_project",
        operation_description="Endpoint for the creation of a project",
        operation_summary="Create a project",
        request_body=CreateProjectSerializer(),
        responses={
            201: ProjectSerializer(),
            400: '{"error": "Invalid data provided for project creation"}',
            404: '{"error": "You are not connected !"}',
            500: '{"error": "Project creation failed"}',
        },
        tags=["Projects"],
        security=[{"Bearer": []}],
    )
    @check_user_is_connected
    def post(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        if not serialized.is_valid():
            logging.exception(serialized.errors)
            return Response(
                {"error": "Invalid data provided for project creation"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        connected_user = get_connected_user(request)
        validated_data = serialized.validated_data
        use_case = CreateProjectUseCase(ProjectRepository(), UserRepository())

        try:
            project = use_case.execute(
                owner_id=connected_user.id,
                title=validated_data["title"],
                description=validated_data.get("description"),
            )

            return Response(
                ProjectSerializer(project).data, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logging.exception(f"Error during project creation: {e}")
            return Response(
                {"error": "Project creation failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class EditProjectAPIView(APIView):
    serializer_class = EditProjectSerializer

    @swagger_auto_schema(
        operation_id="edit_project",
        operation_description="Endpoint for the editing of a project",
        operation_summary="Edit a project",
        request_body=EditProjectSerializer(),
        responses={
            200: ProjectSerializer(),
            400: '{"error": "Invalid data provided for project editing"}',
            404: '{"error": "You are not connected !"}',
            500: '{"error": "Project editing failed"}',
        },
        tags=["Projects"],
        security=[{"Bearer": []}],
    )
    @check_user_is_connected
    def put(self, request, id: str, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        if not serialized.is_valid():
            logging.exception(serialized.errors)
            return Response(
                {"error": "Invalid data provided for project editing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        connected_user = get_connected_user(request)
        validated_data = serialized.validated_data
        use_case = EditProjectUseCase(ProjectRepository(), UserRepository())

        try:
            updated_project = use_case.execute(
                owner_id=connected_user.id,
                project_id=id,
                title=validated_data.get("title"),
                description=validated_data.get("description"),
            )

            return Response(
                ProjectSerializer(updated_project).data, status=status.HTTP_200_OK
            )

        except Exception as e:
            logging.exception(f"Error during project editing: {e}")
            return Response(
                {"error": "Project editing failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteProjectAPIView(APIView):

    @swagger_auto_schema(
        operation_id="delete_project",
        operation_description="Endpoint for the deletion of a project",
        operation_summary="Delete a project",
        responses={
            200: '{"message": "Project deleted successfully !"}',
            404: '{"error": "You are not connected !"}',
            500: '{"error": "Project deletion failed"}',
        },
        tags=["Projects"],
        security=[{"Bearer": []}],
    )
    @check_user_is_connected
    def delete(self, request, id: str, *args, **kwargs):
        connected_user = get_connected_user(request)
        use_case = DeleteProjectUseCase(ProjectRepository(), UserRepository())

        try:
            _ = use_case.execute(owner_id=connected_user.id, project_id=id)

            return Response(
                {"message": "Project deleted successfully !"}, status=status.HTTP_200_OK
            )

        except Exception as e:
            logging.exception(f"Error during project editing: {e}")
            return Response(
                {"error": "Project deletion failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
