from django.db import models
from .Orders import Orders

class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., Cash, Card, Transfer
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class SplitPayment(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='split_payments')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    currency = models.CharField(max_length=3, default='USD') # Assuming USD as default, can be changed
    amount_paid_by_customer = models.DecimalField(max_digits=10, decimal_places=2)
    change_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reference = models.CharField(max_length=255, blank=True, null=True)  # Optional reference field
    notes = models.TextField(blank=True, null=True)  # Optional notes field
    is_refunded = models.BooleanField(default=False, null=True)  # Flag to track if payment is refunded
    refunded_at = models.DateTimeField(blank=True,null=True)  # Date and time when payment was refunded

    def __str__(self):
        return f"Split payment for Order {self.order.id} via {self.payment_method.name}"

    class Meta:
        verbose_name = 'Split Payment'
        verbose_name_plural = 'Split Payments'