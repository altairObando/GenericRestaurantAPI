from django.db import models
from .Contact import Contact

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, null=True, blank=True)
    owner = models.ForeignKey(Contact, on_delete=models.CASCADE)
    tags  = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name