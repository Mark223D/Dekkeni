# Generated by Django 2.2.1 on 2019-07-25 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='superuser',
            field=models.BooleanField(default=False),
        ),
    ]
