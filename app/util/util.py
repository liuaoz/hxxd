import uuid


def generate_uuid():
    """
    generate uuid, and return the last 10 characters
    """
    return str(uuid.uuid4()).replace("-", "")[-10:]
