# Generated by Django 3.2.23 on 2024-06-02 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0048_user_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(help_text='Frequently asked question.')),
                ('answer', models.TextField(blank=True, help_text='Answer to the question.', null=True)),
                ('is_faq', models.BooleanField(default=False, help_text='Designates whether the entry is an approved FAQ.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]