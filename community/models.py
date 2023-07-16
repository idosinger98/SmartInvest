from django.db import models
from django.utils import timezone
from django.db.models import F, Count
from users.models import Profile
from stockAnalysis.models import AnalyzedStocks


class PostManager(models.Manager):

    def sort_posts_by_time(self):
        return self.get_queryset().order_by('-time')

    def sort_posts_by_popularity(self):
        return self.get_queryset().annotate(
            popularity=(5 * Count('comment', distinct=True)) + Count('likes', distinct=True)).order_by('-popularity')

    def sort_posts_by_likes(self):
        return self.get_queryset().annotate(popularity=Count('likes')).order_by('-popularity')

    def sort_posts_by_comments(self):
        return self.get_queryset().annotate(popularity=Count('comment')).order_by('-popularity')

    def get_posts_by_publisher_id(self, publisher_id: int):
        analyzed_stocks_list = AnalyzedStocks.objects.get_user_stocks(analyst_id=publisher_id)
        return self.filter(analysis_id__in=analyzed_stocks_list)

    # def get_amount_of_likes(self, post_id):
    #     return Post.objects.get(pk=post_id).count('likes')

    def like_post(self, post_id, profile_id):
        post = Post.objects.get(id=post_id)
        profile = Profile.objects.get(pk=profile_id)
        post.likes.add(profile)
        post.save()

    def unlike_post(self, post_id, profile_id):
        post = Post.objects.get(id=post_id)
        profile = Profile.objects.get(pk=profile_id)
        post.likes.remove(profile)
        post.save()

    def check_if_profile_liked_the_post(self, post_id, profile_id):
        profile = Profile.objects.get(pk=profile_id)
        post = Post.objects.get(pk=post_id)
        return profile in post.likes.all()


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    analysis_id = models.OneToOneField(AnalyzedStocks, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default='No Title')
    likes = models.ManyToManyField(Profile, blank=True)
    time = models.DateTimeField(default=timezone.now)
    objects = PostManager()


class CommentManager(models.Manager):

    def get_all_comments_on_post(self, post_id: int):
        return self.filter(post_id__id=post_id)

    def sort_comments_by_time(self, post_id: int):
        return self.get_all_comments_on_post(post_id=post_id).order_by('-time')

    def sort_comments_by_likes(self, post_id: int):
        return self.get_queryset().annotate(likes_count=models.Count('likes')).order_by('-likes_count')

    def like_comment(self, comment_id, profile_id):
        comment = Comment.objects.get(id=comment_id)
        profile = Profile.objects.get(pk=profile_id)
        comment.likes.add(profile)
        comment.save()

    def unlike_comment(self, comment_id, profile_id):
        comment = Comment.objects.get(id=comment_id)
        profile = Profile.objects.get(pk=profile_id)
        comment.likes.remove(profile)
        comment.save()

    def comment_post(self, post_id, content, publisher_id):
        comment = Comment.objects.create(publisher_id=publisher_id, content=content, post_id=post_id)
        comment.save()
        return comment

    def check_if_profile_liked_the_comment(self, comment_id, profile_id):
        profile = Profile.objects.get(pk=profile_id)
        comment = Comment.objects.get(pk=comment_id)
        return profile in comment.likes.all()


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    publisher_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='published_comments')
    content = models.TextField()
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Profile, blank=True, related_name='liked_comments')
    time = models.DateTimeField(default=timezone.now)
    objects = CommentManager()
