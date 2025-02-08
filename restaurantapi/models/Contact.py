from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=1)

    def __str__(self):
        return '{0} {1} {2}'.format(self.name, self.middle_name, self.last_name)