
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stockAnalysis', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('likes', models.IntegerField(default=0)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('analysis_id', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='stockAnalysis.analyzedstock'
                 )),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.post')),
                ('publisher_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
