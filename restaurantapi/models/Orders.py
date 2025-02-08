from django.db import models
from .Restaurant import Restaurant
from .Waiters import Waiter
from .RestaurantLocations import RestaurantLocations

ORDER_STATUS = (
    ('RESERVED', 'RESERVED'),
    ('ACTIVE', 'ACTIVE'),
    ('DELIVERED', 'DELIVERED'),
    ('CANCELLED', 'CANCELLED'),
    ('PAID', 'PAID'),
)

class Orders(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    waiter = models.ForeignKey(Waiter, on_delete=models.CASCADE)
    location = models.ForeignKey(RestaurantLocations, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default='RESERVED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return self.order_status

class OrderDetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='OrderDetails_set')
    item_name = models.CharField(max_length=100)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'

    def __str__(self):
        return self.item_name
