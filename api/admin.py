from django.contrib import admin

from api.models import Profile, Invitation


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin options for Profile model
    """
    list_display = ('id', 'user', 'code', 'referred_by', 'created_at', 'updated_at')


class InvitationAdmin(admin.ModelAdmin):
    """
    Admin options for Invitation model
    """
    list_display = ('id', 'email', 'link', 'expired', 'expiry_at', 'created_by', 'created_at', 'updated_at')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Invitation, InvitationAdmin)
