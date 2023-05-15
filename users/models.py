from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    profile_id = models.BigAutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    birthday = models.DateField()
