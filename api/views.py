import datetime
import uuid

from django.contrib.auth.models import User
from django.core.mail import send_mail
from pytz import utc
from rest_framework import viewsets, permissions, status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response

from api.models import Invitation, Profile
from api.serializers import InvitationSerializer, UserSerializer, ProfileSerializer


# Create your views here.
class InvitationViewSet(viewsets.ModelViewSet):
    """
    API viewset for Invitation model
    """
    serializer_class = InvitationSerializer
    queryset = Invitation.objects.all().order_by('-created_at')
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
        # This will not send an email as the email host is `localhost`.
        # The email will be printed on the console.
        send_mail(
            subject="Invitation",
            message=f"Here is your invite link: {link}",
            from_email="noreply@ref.com",
            recipient_list=[serializer.data.get('email')]
        )


class SignupViewSet(viewsets.ModelViewSet, CreateModelMixin):
    """
    API viewset for user signup
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.perform_create(serializer)

        if response is not None:
            return response

        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Signup successful.'}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        invitation = Invitation.objects.get(link=self.request.build_absolute_uri())

        # Check if the invite url is valid
        if invitation is not None:
            if invitation.expired or datetime.datetime.now().replace(tzinfo=utc) > invitation.expiry_at:
                # Expire the invitation
                invitation.expired = True
                invitation.save()

                return Response({'message': 'Invitation link is expired.'}, status=400)
            else:
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

                # Expire the invitation
                invitation.expired = True
                invitation.save()

                return None

        else:
            return Response({'message': 'Invalid link.'}, status=400)


class ReferredUsersViewSet(viewsets.ModelViewSet, ListModelMixin):
    """
    API viewset to get referred users
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all().order_by('-created_at')
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Profile.objects.filter(referred_by__id=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
