# Generated by Django 3.0.5 on 2020-04-21 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0002_auto_20200413_0429'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
