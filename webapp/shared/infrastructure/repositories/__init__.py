from abc import ABC, abstractmethod


class BaseRepository(ABC):
    """Abstract base repository interface"""

    @abstractmethod
    def get_by_id(self, *args):
        """Get entity by ID"""
        pass

    @abstractmethod
    def create(self, **kwargs):
        """Create new entity"""
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        """Update entity"""
        pass

    @abstractmethod
    def delete(self, *args):
        """Delete entity"""
        pass


class UserRepositoryInterface(ABC):
    """Interface for user repository"""

    @abstractmethod
    def get_by_username(self, *args):
        pass

    @abstractmethod
    def get_by_email(self, *args):
        pass

    @abstractmethod
    def exists_by_username(self, *args) -> bool:
        pass

    @abstractmethod
    def exists_by_email(self, *args) -> bool:
        pass

    @abstractmethod
    def check_password(self, *args) -> bool:
        pass


class ProjectRepositoryInterface(ABC):
    """Interface for project repository"""

    @abstractmethod
    def get_by_owner(self, *args, **kwargs):
        pass

    @abstractmethod
    def is_owned_by(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_with_time_spent(self, **kwargs):
        pass


class TaskRepositoryInterface(ABC):
    """Interface for task repository"""

    @abstractmethod
    def get_by_project(self, **kwargs):
        pass

    @abstractmethod
    def get_by_user(self, **kwargs):
        pass

    @abstractmethod
    def update_spent_time(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_tasks_by_status_count(self, **kwargs):
        pass

    @abstractmethod
    def get_tasks_time_summary(self, **kwargs):
        pass


class TimeEntryRepositoryInterface(ABC):
    """Interface for time entry repository"""

    @abstractmethod
    def get_active_timer_for_user(self, **kwargs):
        pass

    @abstractmethod
    def get_active_timer_for_task(self, **kwargs):
        pass

    @abstractmethod
    def has_active_timer(self, **kwargs) -> bool:
        pass

    @abstractmethod
    def stop_active_timers_for_user(self, **kwargs):
        pass
    
    @abstractmethod
    def get_by_user(self, **kwargs):
        pass
