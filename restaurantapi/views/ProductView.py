from rest_framework import generics, validators
from ..models import * 
from ..serializers import *

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        restaurantId = self.request.query_params.get('restaurantId', None)
        ownerId = self.request.ownerId
        if ownerId is None or ownerId == '':
            raise validators.ValidationError({'ownerId': 'This field is required.'})
        q1 = super().get_queryset().filter(restaurant__owner__id=ownerId)
        if restaurantId is None:
            return q1
        return q1.filter(restaurant__id=restaurantId)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer