# Generated by Django 2.2.1 on 2019-06-08 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_auto_20190608_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_holder_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]