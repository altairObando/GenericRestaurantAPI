from django.db import models
from .Contact import Contact

class Waiter(models.Model):
    nif = models.CharField(max_length=20, unique=True)
    contact  = models.ForeignKey(Contact, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)

    def __str__(self):
        return self.name