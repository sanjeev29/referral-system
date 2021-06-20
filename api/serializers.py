from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Invitation


class InvitationSerializer(serializers.ModelSerializer):
    """
    Invitation model serializer
    """

    class Meta:
        model = Invitation
        fields = ['email', 'link', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['link', 'created_by']


class UserSerializer(serializers.ModelSerializer):
    """
    User model serializer
    """
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
