# Generated by Django 3.2.23 on 2024-05-10 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0046_user_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]