from django.db import models
from .Products import Product

class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    valid_to = models.DateField(null=True, blank=True)
    is_extra = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name + " - " + str(self.price)
    
    class Meta:
        verbose_name = 'Product Price'
        verbose_name_plural = 'Product Prices'