# Generated by Django 3.2.23 on 2024-04-05 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_auto_20231227_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='nearby_attractions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='plots_available',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='sq_ft_from',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
