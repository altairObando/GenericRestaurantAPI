from rest_framework import generics, validators
from ..models import * 
from ..serializers import *

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        restaurantId = self.request.query_params.get('restaurantId', None)
        ownerId = self.request.query_params.get('ownerId', None)
        if restaurantId is None or restaurantId == '':
            raise validators.ValidationError({'restaurantId': 'This field is required.'})
        if ownerId is None or ownerId == '':
            raise validators.ValidationError({'ownerId': 'This field is required.'})
        return super().get_queryset().filter(restaurant__id=restaurantId).filter(restaurant__owner__id=ownerId)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class PricingList(generics.ListCreateAPIView):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer

    def get_queryset(self):
        productId = self.request.query_params.get('productId', None)
        if productId is None or productId == '':
            raise validators.ValidationError({'productId': 'This field is required.'})
        return super().get_queryset().filter(product__id=productId)
class PricingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer