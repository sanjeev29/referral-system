from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import InvitationViewSet, SignupViewSet, ReferredUsersViewSet

router = DefaultRouter()

router.register('invitations', InvitationViewSet)
router.register('signup', SignupViewSet)
router.register('referred_users', ReferredUsersViewSet)

urlpatterns = [
    path('', include(router.urls))
]
