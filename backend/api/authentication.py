from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from .models import ActivityLog

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Log successful login
        ActivityLog.objects.create(
            user=user,
            actionType='USER_LOGIN',
            description=f"User {user.username} logged in successfully"
        )
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'role': user.role
        }, status=status.HTTP_200_OK)