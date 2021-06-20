import uuid

from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from api.models import Invitation, Profile
from api.serializers import InvitationSerializer, UserSerializer


# Create your views here.
class InvitationViewSet(viewsets.ModelViewSet):
    """
    API viewset for Invitation model
    """
    serializer_class = InvitationSerializer
    queryset = Invitation.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Invitation.objects.filter(created_by__id=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user_profile = Profile.objects.get(user__id=self.request.user.id)
        link = f'http://localhost:8000/api/v1/signup/?code={user_profile.code}{uuid.uuid4().hex.upper()[:6]}'

        if Invitation.objects.filter(link=link).exists():
            link = f'http://localhost:8000/api/v1/signup/?code={user_profile.code}{uuid.uuid4().hex.upper()[:6]}'

        serializer.save(
            link=link,
            created_by=user_profile.user
        )

        # Send invite email to user


class SignupViewSet(viewsets.ModelViewSet, CreateModelMixin):
    """
    API viewset for user signup
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Signup successful.'}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # Check if the invite url is valid
        if not Invitation.objects.filter(link=self.request.build_absolute_uri()).exists():
            code = self.request.query_params.get('code', default=None)

            user_profile = Profile.objects.get(code=code[:12])
            if user_profile is None:
                return Response({'message': 'Invalid link.'}, status=400)

            serializer.save()

            # Get user by email
            user = User.objects.get(email=serializer.data.get('email'))

            # Create a profile for the new user
            Profile.objects.create(
                user=user,
                referred_by=user_profile.user
            )

        else:
            return Response({'message': 'Invalid link.'}, status=400)
