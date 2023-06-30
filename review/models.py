from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import Profile


class ReviewManager(models.Manager):
    def get_all_reviews(self):
        return self.all()

    def get_last_five_reviews(self):
        return self.order_by('-date')[:5]


class Review(models.Model):
    review_id = models.BigAutoField(primary_key=True)
    publisher_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    date = models.DateTimeField(default=timezone.now)
    objects = ReviewManager()
