from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Invitation, Profile


class InvitationSerializer(serializers.ModelSerializer):
    """
    Invitation model serializer
    """

    class Meta:
        model = Invitation
        fields = ['email', 'link', 'expired', 'expiry_at', 'created_at', 'updated_at']
        read_only_fields = ['link']


class UserSerializer(serializers.ModelSerializer):
    """
    User model serializer
    """
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile model serializer
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'email']
