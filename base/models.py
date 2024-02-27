from django.db import models
from django.contrib.auth.models import AbstractUser
 
class CustomUser(AbstractUser):
    # Add any additional attributes here (e.g. phone
    age = models.PositiveIntegerField(blank=True, null=True)