import uuid


def generate_uuid() -> str:
    """Generate a string UUID"""
    return uuid.uuid4().hex
