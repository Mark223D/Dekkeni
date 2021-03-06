# Generated by Django 2.2.1 on 2019-06-08 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_billingprofile_customer_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', models.CharField(blank=True, max_length=120, null=True)),
                ('brand', models.CharField(blank=True, max_length=120, null=True)),
                ('country', models.CharField(blank=True, max_length=20, null=True)),
                ('exp_month', models.IntegerField()),
                ('exp_year', models.IntegerField()),
                ('last4', models.CharField(blank=True, max_length=4, null=True)),
                ('billing_profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='billing.BillingProfile')),
            ],
        ),
    ]
