from django.test import TestCase


LIKES = 0
ANALYZE_ID_0 = 0
ANALYZE_ID_1 = 1


@pytest.fixture
# make_analyzedStocks
def make_post():
    def make(
        # analysis_id: AnalyzedStocks = make_analyzedStocks(),
        analysis_id: int = ANALYZE_ID_0,
        likes: int = LIKES,
        date: DateTime = timezone.now,

    ):
        post = Post.objects.create(analysis_id=analysis_id, likes=likes, date=date)
        return post

    return make
