from django.db import models
from .Products import ProductCategory
from .ProductPrice import ProductPrice as Price

class Menu(models.Model):
    restaurant = models.ForeignKey('restaurantapi.restaurant', models.CASCADE)
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class MenuCategories(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='categories')
    cate = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return "{0} - {1}".format(self.menu.name, self.cate.name)

class MenuPrices(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT, related_name='prices')
    price = models.ForeignKey(Price, on_delete=models.PROTECT)

    def __str__(self):
        return "{0} - {1} {2}".format(self.menu.name, self.price.product.name, self.price.price )
