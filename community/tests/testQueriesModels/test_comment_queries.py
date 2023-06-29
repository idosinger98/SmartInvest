import pytest
from community.models import Comment
from stockAnalysis.tests.testQueriesModel import test_user
from django.utils import timezone
from datetime import timedelta


DELTA = timedelta(hours=1)


@pytest.mark.django_db
class TestCommentManager:
    def test_sort_comments_by_time(self, make_post, make_comment, test_user):
        post = make_post()
        publisher = test_user
        time_1 = timezone.now() + DELTA
        comment_1 = make_comment(publisher_id=publisher, post_id=post, time=time_1)
        time_2 = time_1 + DELTA
        comment_2 = make_comment(publisher_id=publisher, post_id=post, time=time_2)
        time_3 = time_2 + DELTA
        comment_3 = make_comment(publisher_id=publisher, post_id=post, time=time_3)
        assert Comment.objects.sort_comments_by_time(post_id=post.id)[0] == comment_3
        assert Comment.objects.sort_comments_by_time(post_id=post.id)[1] == comment_2
        assert Comment.objects.sort_comments_by_time(post_id=post.id)[2] == comment_1

    def test_sort_comments_by_likes(self, make_post, make_comment, test_user):
        post = make_post()
        publisher = test_user
        comment_1 = make_comment(publisher_id=publisher, post_id=post, likes=2)
        comment_2 = make_comment(publisher_id=publisher, post_id=post, likes=3)
        comment_3 = make_comment(publisher_id=publisher, post_id=post, likes=1)
        assert Comment.objects.sort_comments_by_likes(post_id=post.id)[0] == comment_2
        assert Comment.objects.sort_comments_by_likes(post_id=post.id)[1] == comment_1
        assert Comment.objects.sort_comments_by_likes(post_id=post.id)[2] == comment_3
