from django.urls import path, include
from rest_framework.routers import DefaultRouter
from coreapp.views import UserProfileViewSet, AvatarUpdateView

router = DefaultRouter()
router.register(r"profiles", UserProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("avatar/", AvatarUpdateView.as_view(), name="avatar_update")
]