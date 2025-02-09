from django.db import models
from .Restaurant import Restaurant
from datetime import datetime

class ProductCategory(models.Model):
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Product(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=250)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    def __str__(self):
        return self.name
    def get_price(self) -> str:
        current_price = self.productprice_set.filter(valid_to__gte=datetime.now()).first()
        current_extra = self.productprice_set.filter(valid_to__gte=datetime.now()).filter(is_extra=True).first()
        if not current_price and not current_extra:
            return "No price available"
        if current_price and current_extra:
            return f"Price: {current_price.price} - As Extra: {current_extra.price}"
        return f"Price: {current_price.price}" if current_price else f"Extra: {current_extra.price}"
        