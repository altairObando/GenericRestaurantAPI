# Generated by Django 5.1.6 on 2025-05-26 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantapi', '0014_paymentmethod_splitpayment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordertaxes',
            options={'verbose_name': 'Order Taxes', 'verbose_name_plural': 'Order Taxes'},
        ),
    ]
