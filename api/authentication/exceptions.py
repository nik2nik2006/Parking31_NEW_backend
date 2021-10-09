from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        return Response(
            {
                "error": {
                    "code": 400,
                    "message": "Unauthorized!"
                }
            }, status=status.HTTP_400_BAD_REQUEST
        )

    elif isinstance(exc, AuthenticationFailed):
        return Response(
            {
                "error": {
                    "code": 401,
                    "message": "Access token is invalid/expired!"
                }
            }, status=status.HTTP_401_UNAUTHORIZED
        )

    return exception_handler(exc, context)
