# Generated by Django 2.2.5 on 2019-09-30 16:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20190930_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
