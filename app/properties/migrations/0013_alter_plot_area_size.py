# Generated by Django 3.2.23 on 2024-05-07 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0012_alter_plot_is_corner_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plot',
            name='area_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]