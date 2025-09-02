import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from middlewares.auth_middleware import check_user_is_connected
from serializers import ProjectSerializer
from serializers.project_serializer import ProjectsWithTaskStatistics
from utils.user_utils import get_connected_user
from webapp.projects.application.use_cases import (
    CreateProjectUseCase,
    DashboardOverviewUseCase,
    DeleteProjectUseCase,
    EditProjectUseCase,
    ListProjectUseCase,
)
from webapp.projects.infrastructure.repositories import ProjectRepository
from webapp.projects.presentation.serializers import (
    CreateProjectSerializer,
    EditProjectSerializer,
)
from webapp.tasks.infrastructure.repositories import TaskRepository
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


class RetrievePaginatedProjectsAPIView(APIView):

    @swagger_auto_schema(
        operation_id="paginated_projects",
        operation_description="""
        Endpoint for retrieving paginated projects.
        This endpoint will return **projects** with pagination info: **page**, **size**, **total** and **more**
        Filters options can be added to the url.
        
        ## URL PARAMETERS
        ***page***: The current page of the pagination (default = 1)
        ***size***: The size of returned items (default = 5)
        ***query***: The user input for search
        ***status***: The task status value to filtering
        ***start_date*** and ***end_date***: The date range to filtering
        
        ## Example
        GET {BASE_URL}/api/projects/list/?page=1&size=5&query=text&status=done&start_date=2025-09-01
        """,
        operation_summary="Retrieve paginated projects",
        responses={
            200: ProjectSerializer(),
            404: '{"error": "You are not connected !"}',
            500: '{"error": "Projects listing failed"}',
        },
        tags=["Projects"],
        security=[{"Bearer": []}],
    )
    @check_user_is_connected
    def get(self, request, *args, **kwargs):
        page = 1
        size = 5
        query = ""
        filter_status = None
        start_date = None
        end_date = None
        if "page" in request.GET and request.GET["page"].strip() != "":
            page = int(request.GET["page"])

        if "size" in request.GET and request.GET["size"].strip() != "":
            size = int(request.GET["size"])

        if "query" in request.GET and request.GET["query"].strip() != "":
            query = request.GET["query"]

        if "status" in request.GET and request.GET["status"].strip() != "":
            filter_status = request.GET["status"]

        if "start_date" in request.GET and request.GET["start_date"].strip() != "":
            start_date = request.GET["start_date"]

        if "end_date" in request.GET and request.GET["end_date"].strip() != "":
            end_date = request.GET["end_date"]

        connected_user = get_connected_user(request)
        use_case = ListProjectUseCase(ProjectRepository(), UserRepository())

        try:
            paginated_projects = use_case.execute(
                owner_id=connected_user.id,
                page=page,
                size=size,
                query=query,
                status=filter_status,
                start_date=start_date,
                end_date=end_date,
            )

            paginated_projects.update(
                {
                    "projects": ProjectsWithTaskStatistics(
                        paginated_projects["projects"], many=True
                    ).data
                }
            )

            return Response(paginated_projects, status=status.HTTP_200_OK)

        except Exception as e:
            logging.exception(f"Error during projects listing: {e}")
            return Response(
                {"error": "Projects listing failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DashboardOverviewAPIView(APIView):

    @swagger_auto_schema(
        operation_id="dashboard_overview",
        operation_description="""
        Endpoint for retrieving dashboard overview on projects and tasks.
        """,
        operation_summary="Retrieve dashboard overview data",
        responses={
            200: "Dashboard Overview Data",
            401: '{"error": "You are not connected !"}',
            500: '{"error": "Dashboard overview retrieving failed"}',
        },
        tags=["Projects"],
        security=[{"Bearer": []}],
    )
    @check_user_is_connected
    def get(self, request, *args, **kwargs):
        connected_user = get_connected_user(request)
        use_case = DashboardOverviewUseCase(
            ProjectRepository(), TaskRepository(), UserRepository()
        )

        try:
            dashboard_overview = use_case.execute(user_id=connected_user.id)
            return Response(dashboard_overview, status=status.HTTP_200_OK)

        except Exception as e:
            logging.exception(f"Error during the dashboard overview retrieving: {e}")
            return Response(
                {"error": "Dashboard overview retrieving failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
