from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator
from django_countries.fields import CountryField


class Profile(models.Model):
    profile_id = models.BigAutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^[0-9]*$', message='Phone number must be numeric.')
    phone_number = models.CharField(validators=[phone_regex, MinLengthValidator(10)], max_length=10)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    country = CountryField(blank_label='(Select country)')
