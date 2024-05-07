# Generated by Django 3.2.23 on 2024-05-07 05:24

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0012_alter_plot_is_corner_site'),
        ('users', '0029_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorited_by', to='properties.Phase'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='0947d745f97a432cbf3eba4df3f98d21', error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]