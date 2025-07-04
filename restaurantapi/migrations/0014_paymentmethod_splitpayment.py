# Generated by Django 5.1.6 on 2025-05-23 19:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantapi', '0013_orderdetails_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SplitPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(default='USD', max_length=3)),
                ('amount_paid_by_customer', models.DecimalField(decimal_places=2, max_digits=10)),
                ('change_due', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference', models.CharField(blank=True, max_length=255, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('is_refunded', models.BooleanField(default=False, null=True)),
                ('refunded_at', models.DateTimeField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='split_payments', to='restaurantapi.orders')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='restaurantapi.paymentmethod')),
            ],
            options={
                'verbose_name': 'Split Payment',
                'verbose_name_plural': 'Split Payments',
            },
        ),
    ]
