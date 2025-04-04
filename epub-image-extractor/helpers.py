import uuid


def generate_uuid_string(prefix='') -> str:
    """
    Generate a UUID string with a prefix.
    """
    return prefix.replace(' ', '') + str(uuid.uuid4())
