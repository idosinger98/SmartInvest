import pytest
from django.utils import timezone
from datetime import timedelta
from community.models import Post


DELTA = timedelta(days=1)


@pytest.mark.django_db
class TestPostManager:
    def test_like_post(self, make_post, test_user):
        post = make_post()
        Post.objects.like_post(post_id=post.id, profile_id=test_user.profile_id)
        post.refresh_from_db()
        assert post.likes.count() == 1

    def test_unlike_post(self, make_post, test_user):
        post = make_post(likes=[test_user])
        Post.objects.unlike_post(post_id=post.id, profile_id=test_user.profile_id)
        post.refresh_from_db()
        assert post.likes.count() == 0

    def test_check_if_profile_liked_the_post(self, make_post, test_user):
        post = make_post(likes=[test_user])
        assert Post.objects.check_if_profile_liked_the_post(post_id=post.id, profile_id=test_user.profile_id) is True

    def test_sort_posts_by_time(self, make_post, test_analyzed_stock, test_analyzed_stock2, test_analyzed_stock3):
        analyzed_stock_1 = test_analyzed_stock
        time_1 = timezone.now() + DELTA
        analyzed_stock_2 = test_analyzed_stock2
        time_2 = time_1 + DELTA
        analyzed_stock_3 = test_analyzed_stock3
        time_3 = time_2 + DELTA
        post_1 = make_post(analysis_id=analyzed_stock_1, time=time_1)
        post_2 = make_post(analysis_id=analyzed_stock_2, time=time_2)
        post_3 = make_post(analysis_id=analyzed_stock_3, time=time_3)

        print(Post.objects.sort_posts_by_time())

        assert Post.objects.sort_posts_by_time()[0] == post_3
        assert Post.objects.sort_posts_by_time()[1] == post_2
        assert Post.objects.sort_posts_by_time()[2] == post_1

    def test_sort_posts_by_popularity(self, make_post, make_comment,
                                      test_user, test_user2, test_user3, test_user4, test_user5,
                                      test_analyzed_stock, test_analyzed_stock2, test_analyzed_stock3):
        analyzed_stock_1 = test_analyzed_stock
        analyzed_stock_2 = test_analyzed_stock2
        analyzed_stock_3 = test_analyzed_stock3

        likes1 = [test_user, test_user2, test_user3]
        likes2 = [test_user, test_user2, test_user3, test_user4]
        likes3 = [test_user, test_user2, test_user3, test_user4, test_user5]

        post_1 = make_post(analysis_id=analyzed_stock_1, likes=likes1)
        post_2 = make_post(analysis_id=analyzed_stock_2, likes=likes2)
        post_3 = make_post(analysis_id=analyzed_stock_3, likes=likes3)

        publisher = test_user

        make_comment(publisher_id=publisher, post_id=post_1)
        make_comment(publisher_id=publisher, post_id=post_1)
        make_comment(publisher_id=publisher, post_id=post_1)
        make_comment(publisher_id=publisher, post_id=post_1)
        make_comment(publisher_id=publisher, post_id=post_1)
        make_comment(publisher_id=publisher, post_id=post_2)
        make_comment(publisher_id=publisher, post_id=post_2)
        make_comment(publisher_id=publisher, post_id=post_2)
        make_comment(publisher_id=publisher, post_id=post_2)
        make_comment(publisher_id=publisher, post_id=post_3)
        make_comment(publisher_id=publisher, post_id=post_3)
        make_comment(publisher_id=publisher, post_id=post_3)

        sorted_posts = Post.objects.sort_posts_by_popularity()

        assert sorted_posts[0] == post_1
        assert sorted_posts[1] == post_2
        assert sorted_posts[2] == post_3

    def test_get_posts_by_publisher_id(self, make_post,
                                       test_analyzed_stock, test_analyzed_stock2, test_analyzed_stock3):
        analyzed_stock_1 = test_analyzed_stock
        analyzed_stock_2 = test_analyzed_stock2
        analyzed_stock_3 = test_analyzed_stock3

        post_1 = make_post(analysis_id=analyzed_stock_1)
        post_2 = make_post(analysis_id=analyzed_stock_2)
        post_3 = make_post(analysis_id=analyzed_stock_3)

        assert Post.objects.get_posts_by_publisher_id(post_1.analysis_id.analyst_id.profile_id)[0] == post_1
        assert Post.objects.get_posts_by_publisher_id(post_2.analysis_id.analyst_id.profile_id)[1] == post_2
        assert Post.objects.get_posts_by_publisher_id(post_3.analysis_id.analyst_id.profile_id)[2] == post_3
