import os
from django.conf import settings
import uuid
from rest_framework_simplejwt.tokens import RefreshToken

def save_file_temporarily(uploaded_file):
    # Generate a temporary file path
    file_name = str(uuid.uuid4()) + '-' + uploaded_file.name
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    # Write the file to disk temporarily
    with open(file_path, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return file_path

def format_error_response(status_code, error_code, message, details=None):
    return {
        "status_code": status_code,
        "error_code": error_code,
        "message": message,
        "details": details or {}
    }



def generate_jwt_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }



def save_file_to_disk(file):
    file_path = os.path.join(settings.MEDIA_ROOT, file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return file_path




import datetime

def parse_iso_datetime(value):
    if isinstance(value, str):
        try:
            return datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError(f"Invalid ISO format for datetime: {value}")
    else:
        raise TypeError(f"Expected string for datetime parsing, got {type(value)}")
