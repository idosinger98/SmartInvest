from django.db import models
from django.utils import timezone
from users.models import Profile


class PostManager(models.Manager):

    def sort_posts_by_date(self):
        return self.get_queryset().order_by('-date')

    def sort_posts_by_likes(self):
        return self.get_queryset().order_by('-likes')

    def sort_posts_by_review_count(self):
        return self.get_queryset().annotate(review_count=models.Count('review')).order_by('-review_count')

    # def get_posts_by_publisher_id(self, publisher_id: int):
        # analyzed_stocks_list = list(AnalyzedStocks.get_all_user_analyzes(id=publisher_id))
        # return self.filter(analysis_id__in=analyzed_stocks_list)


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    analysis_id = models.OneToOneField(AnalyzedStocks, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    objects = PostManager()


class ReviewManager(models.Manager):

    def get_all_reviews_on_post(self, post_id: int):
        return self.filter(post_id__id=post_id)


class Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    publisher_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    objects = ReviewManager()

