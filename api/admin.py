from django.contrib import admin

# Register your models here.
from api.models import Profile, Invitation


class ProfileAdmin(admin.ModelAdmin):
    """
    Admin options for Profile model
    """
    list_display = ('id', 'user', 'code', 'referred_by', 'created_at', 'updated_at')


class InvitationAdmin(admin.ModelAdmin):
    """
    Admin options for Invitation model
    """
    list_display = ('id', 'email', 'link', 'created_by', 'created_at', 'updated_at')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Invitation, InvitationAdmin)
