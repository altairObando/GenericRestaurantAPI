# Generated by Django 5.1.6 on 2025-04-10 18:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantapi', '0008_alter_userprofile_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='waiter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attended_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='active_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restaurantapi.restaurantlocations'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(blank=True, choices=[('OWNER', 'Owner'), ('WAITER', 'Waiter'), ('KITCHEN', 'Kitchen Staff'), ('CASHIER', 'Cashier')], max_length=20, null=True),
        ),
        migrations.DeleteModel(
            name='Waiter',
        ),
    ]
