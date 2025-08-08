import os

SERVER_HOST = os.getenv('SERVER_HOST')


def get_url(file_id):
    if not SERVER_HOST:
        raise ValueError("SERVER_HOST environment variable is not set")
    return f'{SERVER_HOST}/file/{file_id}'
