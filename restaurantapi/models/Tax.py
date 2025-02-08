from django.db import models
from ..models import Orders

class Tax(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    formula = models.CharField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField(auto_now_add=True)
    valid_to = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class OrderTaxes(models.Model):
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.tax.name + " - " + str(self.amount)