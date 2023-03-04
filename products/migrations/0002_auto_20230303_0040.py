# Generated by Django 3.2 on 2023-03-03 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_on']},
        ),
        migrations.AddField(
            model_name='product',
            name='available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=3),
        ),
    ]