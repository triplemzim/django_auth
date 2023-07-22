from django.urls import path
from coreapp.views import UserProfileViewSet

profile_list = UserProfileViewSet.as_view({"get": "list"})
profile_detail = UserProfileViewSet.as_view({"get": "retrieve"})

urlpatterns = [
    path("profile/", profile_list, name="profile-list"),
    path("profile/<str:pk>/", profile_detail, name = "profile-detail"),
]