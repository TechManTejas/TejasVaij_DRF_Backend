from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.contrib.auth import login, get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from user.models import Visit
from .serializers import UserSerializer
import os

class CustomTokenRefreshView(TokenRefreshView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Decode the refresh token to get the user ID
        refresh_token = request.data.get("refresh")
        refresh = RefreshToken(refresh_token)
        user_id = refresh["user_id"]

        # Get the user
        user = get_user_model().objects.get(id=user_id)
        user_serializer = UserSerializer(user)
        serialized_user = user_serializer.data

        return Response(
            {
                "refresh": response.data["refresh"],
                "access": response.data["access"],
                "user": serialized_user,
            }
        )


class UserInfoViewSet(viewsets.ViewSet):

    def list(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    
class VisitViewSet(viewsets.ViewSet):
    def create(self, request):
        user = request.user
        Visit.objects.create(user=user)
        return Response(status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
@transaction.atomic
def google_complete(request):
    client_id = os.getenv("GOOGLE_CLIENT_ID")

    token = request.data.get("token")

    if not token:
        return Response({"error": "Token is missing"}, status=400)

    try:
        idinfo = id_token.verify_oauth2_token(token, Request(), client_id)

        email = idinfo["email"]
        first_name = idinfo.get("given_name", "")
        last_name = idinfo.get("family_name", "")
        profile_picture_url = idinfo.get("picture", "")

        # Check for existing user
        existing_user = get_user_model().objects.filter(username=email).first()

        # Create user
        if not existing_user:
            user = get_user_model().objects.create(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                profile_picture=profile_picture_url,
            )

            user.set_unusable_password()
            user.save()

        else:
            user = existing_user

        login(request, user)
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        serialized_user = user_serializer.data

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": serialized_user,
            }
        )

    except ValueError:
        return Response({"error": "Invalid token"}, status=400)
