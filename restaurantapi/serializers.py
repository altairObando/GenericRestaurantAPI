from .models import *
from rest_framework import serializers

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantLocations
        fields = '__all__'
class RestaurantSerializer(serializers.ModelSerializer):
    locations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    owner = serializers.StringRelatedField(many=False)
    class Meta:
        model = Restaurant
        fields = '__all__'
class WaiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waiter
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
    class Meta:
        model = ProductPrice
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    OrderDetails_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Orders
        fields = '__all__'
class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'