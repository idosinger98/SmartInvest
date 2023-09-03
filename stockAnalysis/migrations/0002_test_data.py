from django.db import migrations, transaction
from users.models import Profile
from stockAnalysis.models import AnalyzedStock


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_test_data'),
        ('stockAnalysis', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):

        analyzed_stock_test_data = [
            (1, {'image': 'static/assets/img/defaultStockImg.jpg'}, 'analysis of aapl stock', False),
            (2, {'image': 'static/assets/img/defaultStockImg.jpg'}, 'analysis of msft stock', False),
            (3, {'image': 'static/assets/img/defaultStockImg.jpg'}, 'analysis of netflix stock', False),
            (4, {'image': 'static/assets/img/defaultStockImg.jpg'}, 'analysis of nvda stock', False),
            (5, {'image': 'static/assets/img/defaultStockImg.jpg'}, 'analysis of ido singer stock - sellll', True),
            (1, {'image': 'static/assets/img/defaultStockImg.jpg'}, 'analysis of general motors stock', False),
        ]
        # Create review
        with transaction.atomic():
            for publisher_id, stock_json, content, public in analyzed_stock_test_data:
                AnalyzedStock(
                    analyst_id=Profile.objects.get(pk=publisher_id),
                    stock_image=stock_json,
                    description=content,
                    is_public=public
                ).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
