# Generated by Django 3.2.23 on 2024-04-30 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0009_plot_is_sold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phase',
            name='status',
            field=models.IntegerField(blank=True, choices=[(1, 'Completed'), (2, 'Not Completed')], default=2, null=True),
        ),
    ]