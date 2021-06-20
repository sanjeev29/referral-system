import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    """
    User profile model
    """
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, blank=True)
    referred_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='ref_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.code == "":
            self.code = uuid.uuid4().hex[:12]

        super(Profile, self).save(*args, **kwargs)


class Invitation(models.Model):
    """
    Invite link model
    """
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField()
    link = models.URLField(unique=True)
    expired = models.BooleanField(default=False)
    expiry_at = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
