from .serializers import *
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import *

class UserProfileViewSet(ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    