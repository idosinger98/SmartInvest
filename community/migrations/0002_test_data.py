from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('community', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        from django.utils import timezone
        from community.models import Post
        test_data = [(1, 0, timezone.now),
                     (2, 1, timezone.now),
                     (3, 2, timezone.now)]
        with transaction.atomic():
            for (analysis_id, likes, date) in test_data:
                post = Post(analysis_id=analysis_id, likes=likes, date=date)
                post.save()

    operations = [
        migrations.RunPython(generate_data),
    ]
