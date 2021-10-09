from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserProfileSerializer
from ..authentication.models import CustomUser
from ..authentication.serializers import UserSerializer


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        serializer = UserProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "error": {
                        "code": 400,
                        "message": serializer.errors
                    }
                }, status=status.HTTP_400_BAD_REQUEST
            )

        user = CustomUser.objects.get(id=request.user.id)

        user.first_name = serializer.validated_data.get('first_name')
        user.last_name = serializer.validated_data.get('last_name')
        user.email = serializer.validated_data.get('email')
        user.address = serializer.validated_data.get('address')
        user.is_profile_completed = True

        user.save()

        return Response(
            {
                "data": {
                    "result": {
                        "user_id": user.id,
                        "is_profile_completed": user.is_profile_completed,
                    },
                    "message": "User profile created successfully!"
                }
            }, status=status.HTTP_200_OK
        )

    @staticmethod
    def get(request):
        user = CustomUser.objects.get(id=request.user.id)

        if not user.is_profile_completed:
            return Response(
                {
                    "error": {
                        "code": 400,
                        "message": "User profile is not completed yet. Please complete first."
                    }
                }, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "data": {
                    "result": UserSerializer(user).data,
                    "message": "User profile is completed."
                }
            }, status=status.HTTP_200_OK
        )
