from django.db import models
from .Restaurant import Restaurant
from .RestaurantLocations import RestaurantLocations
from .Products import Product
ORDER_STATUS = (
    ('RESERVED', 'RESERVED'),
    ('ACTIVE', 'ACTIVE'),
    ('DELIVERED', 'DELIVERED'),
    ('CANCELLED', 'CANCELLED'),
    ('PAID', 'PAID'),
)

class Orders(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    location = models.ForeignKey(RestaurantLocations, on_delete=models.CASCADE, related_name='orders')
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS, default='RESERVED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    waiter = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='attended_orders')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    def __str__(self):
        return self.order_status

class OrderDetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='OrderDetails_set')
    item  = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='OrderDetails_set')
    item_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def item_name(self):
        return self.item.code

    class Meta:
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'

    def __str__(self):
        return self.item_name()
