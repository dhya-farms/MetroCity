# Generated by Django 3.2.23 on 2024-05-07 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0014_alter_plot_soil_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='propertyimage',
            options={'ordering': ['slider_image_order']},
        ),
        migrations.AddField(
            model_name='propertyimage',
            name='is_slider_image',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Use as slider image'),
        ),
        migrations.AddField(
            model_name='propertyimage',
            name='slider_image_order',
            field=models.IntegerField(blank=True, null=True, verbose_name='Slider Image Order'),
        ),
    ]