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
class ProductAdmin(admin.ModelAdmin):
    list_display = [ 'code', 'name', 'category', 'restaurant', 'get_price']
    search_fields = [ 'code', 'name', 'category']
    class Meta:
        model = Product

class Pricing(admin.ModelAdmin):
    list_display = ['id','product', 'price', 'created_on', 'valid_to', 'is_extra']
    search_fields = ['product', 'price']
    class Meta:
        model = ProductPrice        
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurant', 'location', 'order_status', 'subtotal', 'taxes', 'total']
    search_fields = ['restaurant', 'location', 'order_status', 'waiter']
    class Meta:
        model = Orders

class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'item', 'item_price', 'quantity', 'total']
    search_fields = ['order', 'item', 'item_price']
    class Meta:
        model = OrderDetails

class TaxAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'percentage', 'is_active', 'restaurant']
    search_fields = ['name']
    class Meta:
        model = Tax

class OrderTaxesAdmin(admin.ModelAdmin):
    list_display = ['order', 'tax', 'amount']
    search_fields = ['order', 'tax']
    class Meta:
        model = OrderTaxes


admin.site.register(Owner, OwnerAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(RestaurantLocations, RestaurantLocationsAdmin)
admin.site.register(Orders, OrdersAdmin)
admin.site.register(OrderDetails, OrderDetailsAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(OrderTaxes, OrderTaxesAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPrice, Pricing)
admin.site.register(ProductCategory)
admin.site.register(UserProfile)