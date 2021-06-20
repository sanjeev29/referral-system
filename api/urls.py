from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import InvitationViewSet, SignupViewSet

router = DefaultRouter()

router.register('invite', InvitationViewSet)
router.register('signup', SignupViewSet)

urlpatterns = [
    path('', include(router.urls))
]
