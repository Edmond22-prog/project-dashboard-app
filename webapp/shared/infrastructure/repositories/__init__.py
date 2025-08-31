from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseRepository(ABC):
    """Abstract base repository interface"""

    @abstractmethod
    def get_by_id(self, entity_id: str):
        """Get entity by ID"""
        pass

    @abstractmethod
    def create(self, data: Dict[str, Any]):
        """Create new entity"""
        pass

    @abstractmethod
    def update(self, entity, data: Dict[str, Any]):
        """Update entity"""
        pass

    @abstractmethod
    def delete(self, entity):
        """Delete entity"""
        pass


class UserRepositoryInterface(ABC):
    """Interface for user repository"""

    @abstractmethod
    def get_by_username(self, username: str):
        pass

    @abstractmethod
    def get_by_email(self, email: str):
        pass

    @abstractmethod
    def exists_by_username(self, username: str) -> bool:
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass
    
    @abstractmethod
    def check_password(self, username: str, password: str) -> bool:
        pass


class ProjectRepositoryInterface(ABC):
    """Interface for project repository"""

    @abstractmethod
    def get_by_owner(self, user):
        pass

    @abstractmethod
    def get_with_task_statistics(self, user):
        pass

    @abstractmethod
    def search(self, user, search_term: str):
        pass


class TaskRepositoryInterface(ABC):
    """Interface for task repository"""

    @abstractmethod
    def get_by_project(self, project):
        pass

    @abstractmethod
    def get_by_user(self, user):
        pass

    @abstractmethod
    def search(self, user, search_term: str, project_id: Optional[str] = None):
        pass

    @abstractmethod
    def filter_by_status(self, user, status: str, project_id: Optional[str] = None):
        pass


class TimeEntryRepositoryInterface(ABC):
    """Interface for time entry repository"""

    @abstractmethod
    def get_active_timer_for_user(self, user):
        pass

    @abstractmethod
    def get_active_timer_for_task(self, task, user=None):
        pass

    @abstractmethod
    def has_active_timer(self, task) -> bool:
        pass

    @abstractmethod
    def stop_active_timers_for_user(self, user):
        pass
