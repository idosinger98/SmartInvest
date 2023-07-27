from django.db import models
from django.utils import timezone
from django.db.models import F, Count
from users.models import Profile
from stockAnalysis.models import AnalyzedStock


class PostManager(models.Manager):

    def sort_posts_by_time(self):
        return self.get_queryset().order_by('-time')

    def sort_posts_by_popularity(self):
        return self.annotate(popularity=F('likes') + 5 * Count('comment')).order_by('-popularity')

    def get_posts_by_publisher_id(self, publisher_id: int):
        analyzed_stocks_list = AnalyzedStock.objects.get_user_stocks(analyst_id=publisher_id)
        return self.filter(analysis_id__in=analyzed_stocks_list)


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    analysis_id = models.OneToOneField(AnalyzedStock, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)
    objects = PostManager()


class CommentManager(models.Manager):

    def get_all_comments_on_post(self, post_id: int):
        return self.filter(post_id__id=post_id)

    def sort_comments_by_time(self, post_id: int):
        return self.get_all_comments_on_post(post_id=post_id).order_by('-time')

    def sort_comments_by_likes(self, post_id: int):
        return self.get_all_comments_on_post(post_id=post_id).order_by('-likes')


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    publisher_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)
    objects = CommentManager()
