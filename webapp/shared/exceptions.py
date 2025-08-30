class ValidationException(Exception):
    """Domain validation exception"""

    pass


class BusinessRuleException(Exception):
    """Business rule violation exception"""

    pass


class ProjectNotFoundException(Exception):
    """Project not found exception"""

    pass


class TaskNotFoundException(Exception):
    """Task not found exception"""

    pass


class TimerException(Exception):
    """Timer-related exception"""

    pass


class ActiveTimerExistsException(TimerException):
    """Active timer already exists exception"""

    pass


class NoActiveTimerException(TimerException):
    """No active timer found exception"""

    pass


class UnauthorizedAccessException(Exception):
    """Unauthorized access exception"""

    pass
