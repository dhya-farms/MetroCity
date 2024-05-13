# Generated by Django 3.2.23 on 2024-05-10 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm', '0007_alter_payment_payment_for'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='invoice_file',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='online_payment_method',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='online_payment_status',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_type',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='razorpay_invoice_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='razorpay_order_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='razorpay_payment_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='razorpay_signature_id',
        ),
        migrations.RemoveField(
            model_name='statuschangerequest',
            name='approved_by',
        ),
        migrations.AddField(
            model_name='crmlead',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'UPI Payment'), (2, 'Cash Payment'), (3, 'Cheque Payment'), (4, 'Demand Draft'), (5, 'Bank Transfer'), (6, 'Loan')], null=True),
        ),
        migrations.AddField(
            model_name='statuschangerequest',
            name='actioned_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actioned_changes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='statuschangerequest',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_status',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'Completed'), (3, 'Failed')], default=2),
        ),
    ]
