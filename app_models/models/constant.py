from enum import Enum


class TaskStatus(str, Enum):
    """Enum of different task status"""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


TASK_STATUS_CHOICES = tuple([(item.value, item.value) for item in TaskStatus])
