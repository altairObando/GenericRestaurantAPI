from django.db import models

class ContactBase(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

class Owner(ContactBase):
    license_key = models.CharField(max_length=200)
    business_name = models.CharField(max_length=200)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Contact(ContactBase):    
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='contacts')
    def __str__(self):
        return '{0} {1} {2}'.format(self.name, self.middle_name, self.last_name)