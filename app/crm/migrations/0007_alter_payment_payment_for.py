# Generated by Django 3.2.23 on 2024-05-09 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20240508_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_for',
            field=models.IntegerField(choices=[(1, 'Token Advance'), (2, 'Balance')]),
        ),
    ]