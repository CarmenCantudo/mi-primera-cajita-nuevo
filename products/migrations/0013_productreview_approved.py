# Generated by Django 3.2 on 2023-03-28 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20230327_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
