from django.db import migrations, transaction
from django.contrib.auth.models import User
from users.models import Profile


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    def generate_data(apps, schema_editor):
        test_data = [('TalTheUser', 'TalPassword', 'Tal', 'Reinfeld', 'tal@email.com', '111111111', 'US'),
                     ('IdoTheUser', 'TalPassword', 'Ido', 'Singer', 'ido@email.com', '222222222', 'US'),
                     ('Ido2TheUser', 'Ido2Password', 'Ido2', 'Yekutiel', 'ido2@email.com', '333333333', 'US'),
                     ('PatTheUser', 'PatPassword', 'Pat', 'Kaplun', 'pat@email.com', '444444444', 'US'),
                     ('OfirTheUser', 'OfirPassword', 'Ofir', 'Bachar', 'ofir@email.com', '555555555', 'US'),
                     ('GuyTheUser', 'GuyPassword', 'Guy', 'Beckenstain', 'guy@email.com', '666666666', 'US')]
        with transaction.atomic():
            for (username, password, first_name, last_name, email, phone_number, country) in test_data:
                user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                                last_name=last_name, email=email)
                profile = Profile(user_id=user, phone_number=phone_number, country=country)
                profile.user_id.save()
                profile.save()
    operations = [
        migrations.RunPython(generate_data),
    ]