from django.contrib import admin
from .models import *
# Register your models here.
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'license_key', 'business_name']
    search_fields = ['name', 'email', 'license_key']
    class Meta:
        model = Owner

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    search_fields = ['name', 'email']
    class Meta:
        model = Contact

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'address', 'phone', 'owner', 'tags']
    search_fields = ['name', 'description', 'phone']
    class Meta:
        model = Restaurant

class RestaurantLocationsAdmin(admin.ModelAdmin):
    list_display = ['restaurant','parent', 'location']
    search_fields = ['restaurant', 'location']
    ordering = ['parent']
    class Meta:
        model = RestaurantLocations
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(RestaurantLocations, RestaurantLocationsAdmin)