from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    supabase_user_id = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)
