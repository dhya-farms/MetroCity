# Generated by Django 3.2.23 on 2024-05-15 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_file_uploaded_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='related_property',
        ),
    ]