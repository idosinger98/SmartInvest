import pytest
from django.utils import timezone
from datetime import timedelta
from community.models import Post


DELTA = timedelta(days=1)


@pytest.mark.django_db
class TestPostManager:
    # def test_like_post(self, make_post, test_analyzed_stock):
    #     post = make_post(analysis_id=test_analyzed_stock)
    #     old_likes = post.likes
    #     expected_new_likes = old_likes + 1
    #     Post.objects.like_post(post_id=post.id)
    #     post.refresh_from_db()
    #     assert post.likes == expected_new_likes

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

    def test_sort_posts_by_popularity(self, make_post, make_comment, test_user, test_user2, test_user3,
                                      test_analyzed_stock, test_analyzed_stock2, test_analyzed_stock3):
        analyzed_stock_1 = test_analyzed_stock
        analyzed_stock_2 = test_analyzed_stock2
        analyzed_stock_3 = test_analyzed_stock3

        likes1 = [test_user]
        likes2 = [test_user, test_user2]
        likes3 = [test_user, test_user2, test_user3]

        post_1 = make_post(analysis_id=analyzed_stock_1, likes=likes1)
        post_2 = make_post(analysis_id=analyzed_stock_2, likes=likes2)
        post_3 = make_post(analysis_id=analyzed_stock_3, likes=likes3)

        publisher = test_user

        make_comment(publisher_id=publisher, post_id=post_1)
        make_comment(publisher_id=publisher, post_id=post_1)
        make_comment(publisher_id=publisher, post_id=post_2)

        print(Post.objects.all().values)

        assert Post.objects.sort_posts_by_popularity()[0] == post_1
        assert Post.objects.sort_posts_by_popularity()[1] == post_3
        assert Post.objects.sort_posts_by_popularity()[2] == post_1

    def test_get_posts_by_publisher_id(self, make_post, test_user, test_user2, test_user3,
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
