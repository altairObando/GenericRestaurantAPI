from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User,Group
from typing import List, Dict, Optional
from drf_spectacular.utils import extend_schema_field

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
class LocationSerializer(serializers.ModelSerializer):
    sublocations = serializers.SerializerMethodField()
    class Meta:
        model = RestaurantLocations
        fields = '__all__'
        
    @extend_schema_field(List[Dict])
    def get_sublocations(self, obj) -> Optional[List[Dict]]:
        sublocations = obj.sublocations.all()
        if sublocations.count() == 0:
            return None
        return LocationSerializer(sublocations, many=True).data
    
class RestaurantSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    owner = serializers.StringRelatedField(many=False)
    class Meta:
        model = Restaurant
        fields = '__all__'
class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'
class OrderTaxesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTaxes
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
class ProductPriceSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = ProductPrice
        fields = '__all__'

class OrderDetailsSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='item.name', read_only=True)
    
    class Meta:
        model = OrderDetails
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    OrderDetails_set = OrderDetailsSerializer(many=True, read_only=True)
    waiter_name = serializers.CharField(source='waiter.username', read_only=True)
    location_name = serializers.CharField(source='location.location', read_only=True)
    
    class Meta:
        model = Orders
        fields = '__all__'

class MenuPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuPrices
        fields = '__all__'
class MenuCategoriesSerializer(serializers.ModelSerializer):
    class Meta: 
        model = MenuCategories
        fields= '__all__'
class MenuSerializer(serializers.ModelSerializer):
    categories = MenuCategoriesSerializer(many=True, read_only=True)
    prices = MenuPricesSerializer(many=True,read_only=True)
    class Meta:
        model = Menu
        fields = '__all__'
class ProfileSerializer(serializers.ModelSerializer):
    contact = ClientSerializer(many=False, read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['username','email','is_superuser','groups']

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class SplitPaymentSerializer(serializers.ModelSerializer):
    payment_method_name = serializers.CharField(source='payment_method.name', read_only=True)
    order_number = serializers.CharField(source='order.id', read_only=True)
    
    class Meta:
        model = SplitPayment
        fields = '__all__'