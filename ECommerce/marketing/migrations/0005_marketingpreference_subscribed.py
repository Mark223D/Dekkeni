# Generated by Django 2.2.1 on 2019-06-09 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0004_auto_20190609_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketingpreference',
            name='subscribed',
            field=models.BooleanField(default=True),
        ),
    ]
