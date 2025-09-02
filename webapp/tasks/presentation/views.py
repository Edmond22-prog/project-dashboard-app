import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from middlewares.auth_middleware import check_user_is_connected
from serializers import TaskSerializer, TaskTimeEntrySerializer
from utils.user_utils import get_connected_user
from webapp.projects.infrastructure.repositories import ProjectRepository
from webapp.tasks.application.use_cases import (
    CreateTaskUseCase,
    EditTaskUseCase,
    ListTasksUseCase,
    StartTimerUseCase,
    StopTimerUseCase,
)
from webapp.tasks.infrastructure.repositories import TaskRepository, TimeEntryRepository
from webapp.tasks.presentation.serializers import (
    CreateTaskSerializer,
    EditTaskSerializer,
    StartTimerSerializer,
)
from webapp.users.infrastructure.repositories import UserRepository


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


class RetrievePaginatedTasksAPIView(APIView):

    @swagger_auto_schema(
        operation_id="paginated_tasks",
        operation_description="""
        Endpoint for retrieving paginated tasks.
        This endpoint will return **tasks** with pagination info: **page**, **size**, **total** and **more**
        Filters options can be added to the url.
        
        ## URL PARAMETERS
        ***page***: The current page of the pagination (default = 1)
        ***size***: The size of returned items (default = 5)
        ***query***: The user input for search
        ***status***: The status value to filtering
        ***project_id***: The project where to filtering
        
        ## Example
        GET {BASE_URL}/api/tasks/list/?page=1&size=5&query=text&status=done
        """,
        operation_summary="Retrieve paginated tasks",
        responses={
            200: TaskSerializer(),
            404: '{"error": "You are not connected !"}',
            500: '{"error": "Tasks listing failed"}',
        },
        tags=["Tasks"],
        security=[{"Bearer": []}],
    )
    @check_user_is_connected
    def get(self, request, *args, **kwargs):
        page = 1
        size = 5
        query = ""
        filter_status = None
        project_id = None
        if "page" in request.GET and request.GET["page"].strip() != "":
            page = int(request.GET["page"])

        if "size" in request.GET and request.GET["size"].strip() != "":
            size = int(request.GET["size"])

        if "query" in request.GET and request.GET["query"].strip() != "":
            query = request.GET["query"]

        if "status" in request.GET and request.GET["status"].strip() != "":
            filter_status = request.GET["status"]

        if "project_id" in request.GET and request.GET["project_id"].strip() != "":
            project_id = request.GET["project_id"]

        connected_user = get_connected_user(request)
        use_case = ListTasksUseCase(
            ProjectRepository(), UserRepository(), TaskRepository()
        )

        try:
            paginated_tasks = use_case.execute(
                user_id=connected_user.id,
                page=page,
                size=size,
                query=query,
                status=filter_status,
                project_id=project_id,
            )

            paginated_tasks.update(
                {"tasks": TaskSerializer(paginated_tasks["tasks"], many=True).data}
            )

            return Response(paginated_tasks, status=status.HTTP_200_OK)

        except Exception as e:
            logging.exception(f"Error during tasks listing: {e}")
            return Response(
                {"error": "Tasks listing failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class EditTaskAPIView(APIView):
    serializer_class = EditTaskSerializer

    @swagger_auto_schema(
        operation_id="edit_task",
        operation_description="Endpoint for the editing of a task",
        operation_summary="Edit a task",
        request_body=EditTaskSerializer(),
        responses={
            200: TaskSerializer(),
            400: '{"error": "Invalid data provided for task editing"}',
            404: '{"error": "You are not connected !"}',
            500: '{"error": "Task editing failed"}',
        },
        tags=["Tasks"],
        security=[{"Bearer": []}],
    )
    @check_user_is_connected
    def put(self, request, id: str, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        if not serialized.is_valid():
            logging.exception(serialized.errors)
            return Response(
                {"error": "Invalid data provided for task editing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        connected_user = get_connected_user(request)
        validated_data = serialized.validated_data
        use_case = EditTaskUseCase(UserRepository(), TaskRepository())

        try:
            updated_project = use_case.execute(
                user_id=connected_user.id,
                task_id=id,
                title=validated_data.get("title"),
                description=validated_data.get("description"),
                status=validated_data.get("status"),
                estimated_time=validated_data.get("estimated_time"),
            )

            return Response(
                TaskSerializer(updated_project).data, status=status.HTTP_200_OK
            )

        except Exception as e:
            logging.exception(f"Error during task editing: {e}")
            return Response(
                {"error": "Task editing failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class StartTaskTimerAPIView(APIView):
    serializer_class = StartTimerSerializer

    @swagger_auto_schema(
        operation_id="start_timer",
        operation_description="Endpoint for starting a task timer",
        operation_summary="Start a task timer",
        request_body=StartTimerSerializer(),
        responses={
            201: TaskTimeEntrySerializer(),
            400: '{"error": "Invalid data provided for the start timer of a task"}',
            404: '{"error": "You are not connected !"}',
            500: '{"error": "Start timer of the task failed"}',
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
                {"error": "Invalid data provided for the start timer of a task"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        connected_user = get_connected_user(request)
        validated_data = serialized.validated_data
        use_case = StartTimerUseCase(
            TaskRepository(), TimeEntryRepository(), UserRepository()
        )

        try:
            started_timer = use_case.execute(
                user_id=connected_user.id, task_id=validated_data["task_id"]
            )

            return Response(
                TaskTimeEntrySerializer(started_timer).data,
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logging.exception(f"Error during the start timer of a task: {e}")
            return Response(
                {"error": "Start timer of the task failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class StopTaskTimerAPIView(APIView):
    serializer_class = StartTimerSerializer

    @swagger_auto_schema(
        operation_id="stop_timer",
        operation_description="Endpoint for stopping a task timer",
        operation_summary="Stop a task timer",
        request_body=StartTimerSerializer(),
        responses={
            200: "Duration of the task",
            400: '{"error": "Invalid data provided for the stop timer of a task"}',
            404: '{"error": "You are not connected !"}',
            500: '{"error": "Stop timer of the task failed"}',
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
                {"error": "Invalid data provided for the stop timer of a task"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        connected_user = get_connected_user(request)
        validated_data = serialized.validated_data
        use_case = StopTimerUseCase(
            TaskRepository(), TimeEntryRepository(), UserRepository()
        )

        try:
            task_duration = use_case.execute(
                user_id=connected_user.id, task_id=validated_data["task_id"]
            )

            return Response(task_duration, status=status.HTTP_200_OK)

        except Exception as e:
            logging.exception(f"Error during the stop timer of a task: {e}")
            return Response(
                {"error": "Stop timer of the task failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
