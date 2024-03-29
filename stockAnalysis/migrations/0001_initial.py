# Generated by Django 4.2.4 on 2023-08-30 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_test_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockSymbol',
            fields=[
                ('symbol', models.CharField(max_length=7, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='AnalyzedStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_image', models.JSONField()),
                ('description', models.TextField(blank=True)),
                ('is_public', models.BooleanField(default=False)),
                ('analyst_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             to='stockAnalysis.stocksymbol')),
            ],
        ),
    ]
