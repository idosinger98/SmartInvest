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
        ('community', '0002_post_title'),
        ('community', '0003_remove_comment_likes_alter_comment_publisher_id_and_more'),
    ]

    def generate_data(apps, schema_editor):

        post_test_data = [
            (1, 'Post #1', [Profile.objects.get(pk=1)], timezone.now() + DELTA),
            (2, 'Post #2', [Profile.objects.get(pk=1),
                            Profile.objects.get(pk=2)], timezone.now() + DELTA + DELTA),
            (3, 'Post #3', [Profile.objects.get(pk=1),
                            Profile.objects.get(pk=2),
                            Profile.objects.get(pk=3)], timezone.now() + DELTA + DELTA + DELTA),
            (4, 'Post #4', [Profile.objects.get(pk=1),
                            Profile.objects.get(pk=2),
                            Profile.objects.get(pk=3),
                            Profile.objects.get(pk=4)], timezone.now() + DELTA + DELTA + DELTA + DELTA),
            (5, 'Post #5', [Profile.objects.get(pk=1),
                            Profile.objects.get(pk=2),
                            Profile.objects.get(pk=3),
                            Profile.objects.get(pk=4),
                            Profile.objects.get(pk=5)], timezone.now() + DELTA + DELTA + DELTA + DELTA + DELTA),
            # (6, 'Post #6', 6, timezone.now() + DELTA + DELTA + DELTA + DELTA + DELTA + DELTA),
            # (7, 'Post #7', 7, timezone.now() + DELTA + DELTA + DELTA + DELTA + DELTA + DELTA + DELTA)
        ]

        comment_test_data = [
            (1, 'First comment on post 1', 1, [Profile.objects.get(pk=1)], timezone.now()),
            (1, 'Second comment on post 1', 1, [Profile.objects.get(pk=1),
                                                Profile.objects.get(pk=2)], timezone.now() + DELTA),
            (1, 'First comment on post 2', 2, [Profile.objects.get(pk=1)], timezone.now()),
            (1, 'Second comment on post 2', 2, [Profile.objects.get(pk=1),
                                                Profile.objects.get(pk=2)], timezone.now() + DELTA),
            (1, 'First comment on post 3', 3, [Profile.objects.get(pk=1)], timezone.now()),
            (1, 'Second comment on post 3', 3, [Profile.objects.get(pk=1),
                                                Profile.objects.get(pk=2)], timezone.now() + DELTA),
            (1, 'First comment on post 4', 4, [Profile.objects.get(pk=1)], timezone.now()),
            (1, 'Second comment on post 4', 4, [Profile.objects.get(pk=1),
                                                Profile.objects.get(pk=2)], timezone.now() + DELTA),
            (1, 'First comment on post 5', 5, [Profile.objects.get(pk=1)], timezone.now()),
            (1, 'Second comment on post 5', 5, [Profile.objects.get(pk=1),
                                                Profile.objects.get(pk=2)], timezone.now() + DELTA),
            # (1, 'First comment on post 6', 6, 1, timezone.now()),
            # (1, 'Second comment on post 6', 6, 2, timezone.now() + DELTA),
            # (1, 'First comment on post 7', 7, 1, timezone.now()),
            # (1, 'Second comment on post 7', 7, 2, timezone.now() + DELTA),
        ]

        with transaction.atomic():
            for analysis_id, title, profiles, time in post_test_data:
                post = Post.objects.create(
                    analysis_id=AnalyzedStocks.objects.get(pk=analysis_id),
                    title=title,
                    time=time,
                )
                for profile in profiles:
                    post.likes.add(profile)

            post.save()

        with transaction.atomic():
            for publisher_id, content, post_id, profiles, time in comment_test_data:
                comment = Comment.objects.create(
                    publisher_id=Profile.objects.get(pk=publisher_id),
                    content=content,
                    post_id=Post.objects.get(pk=post_id),
                    time=time,
                )
                for profile in profiles:
                    comment.likes.add(profile)

            comment.save()

    operations = [
        migrations.RunPython(generate_data),
    ]
