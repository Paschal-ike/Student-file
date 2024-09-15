from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


from .serializers import AdminRegisterSerializer, AdminLoginSerializer
from .utils import format_error_response, generate_jwt_tokens

class AdminRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = AdminRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Admin user created successfully"}, status=status.HTTP_201_CREATED)
        return Response(
            format_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code='registration_failed',
                message='Registration failed.',
                details=serializer.errors
            ),
            status=status.HTTP_400_BAD_REQUEST
        )

class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = generate_jwt_tokens(user)
            return Response(tokens, status=status.HTTP_200_OK)
        
        return Response(
            format_error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_code='login_failed',
                message='Login failed.',
                details=serializer.errors
            ),
            status=status.HTTP_400_BAD_REQUEST
        )



class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                format_error_response(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    error_code='refresh_token_required',
                    message='Refresh token is required.',
                    details={'refresh': ['This field is required.']}
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            user = refresh.user
            new_tokens = generate_jwt_tokens(user)
            return Response(new_tokens, status=status.HTTP_200_OK)
        except TokenError:
            return Response(
                format_error_response(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    error_code='invalid_token',
                    message='Invalid or expired refresh token.',
                    details={'refresh': ['Invalid or expired token.']}
                ),
                status=status.HTTP_401_UNAUTHORIZED
            )