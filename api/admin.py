from django.contrib import admin

# Register your models here.
from api.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """
    Admin options for Profile model
    """
    list_display = ('id', 'user', 'code', 'referred_by', 'created_at', 'updated_at')


admin.site.register(Profile, ProfileAdmin)
