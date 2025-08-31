from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction

from webapp.shared.infrastructure.repositories import (
    BaseRepository,
    UserRepositoryInterface,
)


class UserRepository(BaseRepository, UserRepositoryInterface):
    """Repository for User entity operations"""

    def get_by_id(self, id):
        """Get user by ID"""
        try:
            return User.objects.get(id=id)

        except User.DoesNotExist:
            return None

    def get_by_username(self, username):
        """Get user by username"""
        try:
            return User.objects.get(username=username)

        except User.DoesNotExist:
            return None

    def get_by_email(self, email):
        """Get user by email"""
        try:
            return User.objects.get(email=email)

        except User.DoesNotExist:
            return None

    def exists_by_username(self, username):
        """Check if user exists by username"""
        return User.objects.filter(username=username).exists()

    def exists_by_email(self, email):
        """Check if user exists by email"""
        return User.objects.filter(email=email).exists()
    
    def check_password(self, username, password):
        """Check if password match the user email"""
        return authenticate(username=username, password=password) is not None

    @transaction.atomic
    def create(self, data):
        """Create new user with password"""
        user = User.objects.create_user(
            username=data["username"],
            email=data["email"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            password=data["password"],
        )
        return user

    def update(self, user, data):
        """Update user data"""
        for field, value in data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        user.save()
        return user

    def delete(self, user):
        """Delete user (soft delete by deactivating)"""
        user.is_active = False
        user.save()
        return user
