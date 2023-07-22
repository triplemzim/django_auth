from django.db import models
import uuid
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user_status = (('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'))

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=user_status, default='ACTIVE')
    level = models.IntegerField(null=False, blank = False, default=1)
    photo = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.user.username
    

