from django.db import migrations, transaction
from users.models import Profile
from stockAnalysis.models import AnalyzedStocks
from community.models import Post, Comment
from django.utils import timezone
from datetime import timedelta


DELTA = timedelta(hours=1)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_test_data'),
        ('stockAnalysis', '0002_test_data'),
        ('community', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        post_test_data = [
            (1, "my first post", "Google Stock Analysis: Key Trends & Performance", 1,
             timezone.now() + DELTA),
            (2, "my second post", "Microsoft: Comprehensive Stock Review", 2,
             timezone.now() + DELTA + DELTA),
            (3, "my third post", "Tesla Stock Analysis: Investment Potential", 3,
             timezone.now() + DELTA + DELTA + DELTA),
            (4, "my fourth post", "Apple: Unraveling Market Performance", 4,
             timezone.now() + DELTA + DELTA + DELTA + DELTA),
            (5, "my five post", "Amazon's Growth Trajectory: A Thorough Stock Analysis", 5,
             timezone.now() + DELTA + DELTA + DELTA + DELTA + DELTA),
        ]

        comment_test_data = [
            (1, 'First comment on post 1', 1, 1, timezone.now()),
            (1, 'Second comment on post 1', 1, 2, timezone.now() + DELTA),
            (1, 'First comment on post 2', 2, 1, timezone.now()),
            (1, 'Second comment on post 2', 2, 2, timezone.now() + DELTA),
            (1, 'First comment on post 3', 3, 1, timezone.now()),
            (1, 'Second comment on post 3', 3, 2, timezone.now() + DELTA),
            (1, 'First comment on post 4', 4, 1, timezone.now()),
            (1, 'Second comment on post 4', 4, 2, timezone.now() + DELTA),
            (1, 'First comment on post 5', 5, 1, timezone.now()),
            (1, 'Second comment on post 5', 5, 2, timezone.now() + DELTA),
        ]

        with transaction.atomic():
            for analysis_id, description, title, likes, time in post_test_data:
                Post(
                    analysis_id=AnalyzedStocks.objects.get(pk=analysis_id),
                    description=description,
                    title=title,
                    likes=likes,
                    time=time,
                ).save()

        with transaction.atomic():
            for publisher_id, content, post_id, likes, time in comment_test_data:
                Comment(
                    publisher_id=Profile.objects.get(pk=publisher_id),
                    content=content,
                    post_id=Post.objects.get(pk=post_id),
                    likes=likes,
                    time=time,
                ).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
