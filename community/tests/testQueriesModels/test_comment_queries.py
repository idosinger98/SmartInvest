import pytest
from community.models import Comment
from django.utils import timezone
from datetime import timedelta


DELTA = timedelta(hours=1)


@pytest.mark.django_db
class TestCommentManager:
    # def test_like_comment(self, make_post, make_comment, test_user):
    #     comment = make_comment(publisher_id=test_user, post_id=make_post())
    #     old_likes = comment.likes
    #     expected_new_likes = old_likes + 1
    #     Comment.objects.like_comment(comment_id=comment.id)
    #     comment.refresh_from_db()
    #     assert comment.likes == expected_new_likes

    def test_comment_post(self, make_post, test_user):
        old_amount_of_comments = Comment.objects.count()
        expected_new_amount_of_comments = old_amount_of_comments + 1
        comment = Comment.objects.comment_post(publisher_id=test_user, content='test comment', post_id=make_post())
        comment.refresh_from_db()
        assert Comment.objects.count() == expected_new_amount_of_comments

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

    def test_sort_comments_by_likes(self, make_post, make_comment, test_user, test_user2, test_user3):
        post = make_post()
        publisher = test_user

        likes1 = [test_user]
        likes2 = [test_user, test_user2]
        likes3 = [test_user, test_user2, test_user3]

        comment_1 = make_comment(publisher_id=publisher, post_id=post, likes=likes1)
        comment_2 = make_comment(publisher_id=publisher, post_id=post, likes=likes2)
        comment_3 = make_comment(publisher_id=publisher, post_id=post, likes=likes3)

        print(Comment.objects.all().values)
        print(Comment.objects.get(pk=13).likes.count())
        print(Comment.objects.get(pk=2).likes.count())

        assert Comment.objects.sort_comments_by_likes(post_id=post.id)[0] == comment_3
        assert Comment.objects.sort_comments_by_likes(post_id=post.id)[1] == comment_2
        assert Comment.objects.sort_comments_by_likes(post_id=post.id)[2] == comment_1
