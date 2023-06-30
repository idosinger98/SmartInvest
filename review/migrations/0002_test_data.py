from datetime import timedelta
from django.db import migrations, transaction
from django.utils import timezone
from users.models import Profile


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
        ('users', '0002_test_data'),
    ]

    def generate_data(apps, schema_editor):
        from review.models import Review

        now = timezone.now()

        # Generate review data
        review_test_data = [
            ('5', 'Excellent!', now - timedelta(days=10), 1),
            ('4', 'Good', now - timedelta(days=20), 2),
            ('3', 'Average', now - timedelta(days=5), 3),
            ('2', 'A simple test review', now - timedelta(days=2), 4),
            ('1', 'Another test review', now - timedelta(days=2), 5),
            ('1', 'Really bad.', now - timedelta(days=2), 6),
        ]
        # Create review
        with transaction.atomic():
            for rating, content, date, publisher_id in review_test_data:
                Review(
                    rating=rating,
                    content=content,
                    date=date,
                    publisher_id=Profile.objects.get(pk=publisher_id)
                ).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
