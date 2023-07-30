from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .models import *
from rest_framework import generics
from rest_framework.filters import SearchFilter

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ["status", "level"]

class AvatarUpdateView(generics.UpdateAPIView):
    serializer_class = PhotoSerializer

    def get_object(self):
        profile_object = self.request.user.userprofile
        return profile_object


        
