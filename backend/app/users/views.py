from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema

from .serializers import (
    UserSerializer,
    RegistrationSerializer,
)


class RegistrationView(generics.CreateAPIView):
    """
    Register a new user account.
    Creates a new user with username, email, and password.
    """
    serializer_class = RegistrationSerializer
    authentication_classes = []
    permission_classes = []


@extend_schema(
    responses={200: UserSerializer},
    description="Get currently authenticated user information"
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def user_me(request):
    """
    Get current user profile information.
    Returns the authenticated user's details.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)