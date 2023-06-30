import pytest
from django.utils import timezone
from datetime import timedelta
from community.models import Post
from django.db.models import F, Count

DELTA = timedelta(hours=1)


@pytest.mark.django_db
class TestPostManager:
    def test_sort_posts_by_date(self, make_post, test_analyzed_stock, test_analyzed_stock2, test_analyzed_stock3):
        analyzed_stock_1 = test_analyzed_stock
        time_1 = timezone.now() + DELTA
        analyzed_stock_2 = test_analyzed_stock2
        time_2 = time_1 + DELTA
        analyzed_stock_3 = test_analyzed_stock3
        time_3 = time_2 + DELTA
        post_1 = make_post(analysis_id=analyzed_stock_1, time=time_1)
        post_2 = make_post(analysis_id=analyzed_stock_2, time=time_2)
        post_3 = make_post(analysis_id=analyzed_stock_3, time=time_3)
        assert Post.objects.sort_posts_by_time()[0] == post_3
        assert Post.objects.sort_posts_by_time()[1] == post_2
        assert Post.objects.sort_posts_by_time()[2] == post_1

    def test_sort_posts_by_popularity(self, make_post, make_comment, test_user,
                                      test_analyzed_stock, test_analyzed_stock2, test_analyzed_stock3):
        analyzed_stock_1 = test_analyzed_stock
        analyzed_stock_2 = test_analyzed_stock2
        analyzed_stock_3 = test_analyzed_stock3

        post_1 = make_post(analysis_id=analyzed_stock_1, likes=1)
        post_2 = make_post(analysis_id=analyzed_stock_2, likes=9)
        post_3 = make_post(analysis_id=analyzed_stock_3, likes=13)

        publisher = test_user

        make_comment(publisher_id=publisher, post_id=post_1)
        make_comment(publisher_id=publisher, post_id=post_1)
        make_comment(publisher_id=publisher, post_id=post_2)

        assert Post.objects.sort_posts_by_popularity()[0] == post_2  # popularity = 14
        assert Post.objects.sort_posts_by_popularity()[1] == post_3  # popularity = 13
        assert Post.objects.sort_posts_by_popularity()[2] == post_1  # popularity = 11
