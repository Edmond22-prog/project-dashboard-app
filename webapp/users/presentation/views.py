import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from serializers.user_serializer import UserSerializer
from webapp.users.application.services import JWTAuthService
from webapp.users.application.use_cases import CreateUserUseCase
from webapp.users.infrastructure.repositories import UserRepository
from webapp.users.presentation.serializers import UserRegistrationSerializer


class RegisterUserAPIView(APIView):
    serializer_class = UserRegistrationSerializer

    @swagger_auto_schema(
        operation_id="register_user",
        operation_description="Endpoint for user registration",
        operation_summary="Register an user",
        request_body=UserRegistrationSerializer(),
        responses={
            201: UserSerializer(),
            400: '{"error": "Invalid data provided for user registration"}',
            500: '{"error": "User registration failed"}',
        },
        tags=["Users"],
        security=[],
    )
    def post(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        if not serialized.is_valid():
            logging.exception(serialized.errors)
            return Response(
                {"error": "Invalid data provided for user registration"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated_data = serialized.validated_data
        use_case = CreateUserUseCase(UserRepository())

        try:
            created_user = use_case.execute(
                username=validated_data["username"],
                email=validated_data["email"],
                first_name=validated_data.get("first_name"),
                last_name=validated_data.get("last_name"),
                password=validated_data["password"],
            )

            # Generate tokens
            auth_service = JWTAuthService()
            tokens = auth_service.generate_tokens(created_user)

            return Response(
                {"user": UserSerializer(created_user).data, "tokens": tokens},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            logging.exception(f"Error during user registration: {e}")
            return Response(
                {"error": "User registration failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
