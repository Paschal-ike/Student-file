from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from rest_framework.exceptions import ValidationError  
from .models import Student
from .utils import format_error_response

def handle_exceptions(func):
    @wraps(func)
    def wrapped_func(self, request, *args, **kwargs):
        try:
            return func(self, request, *args, **kwargs)
        except ValidationError as e:
            error_response = format_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code="VALIDATION_ERROR",
                message="Invalid data provided.",
                details=e.message_dict
            )
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            error_response = format_error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                error_code="STUDENT_NOT_FOUND",
                message="Student not found."
            )
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error_response = format_error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code="INTERNAL_SERVER_ERROR",
                message=str(e)
            )
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapped_func
