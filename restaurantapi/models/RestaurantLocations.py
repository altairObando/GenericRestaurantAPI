from django.db import models
from .Restaurant import Restaurant

class RestaurantLocations(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='locations')
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='sublocations')

    class Meta:
        verbose_name = 'Restaurant Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        activeOrder = self.orders.filter(order_status='ACTIVE').first()
        if activeOrder:
            return f"{self.location} (Active Order: {activeOrder.id})"
        return self.location