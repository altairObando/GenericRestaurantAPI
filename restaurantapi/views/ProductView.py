from rest_framework import generics
from ..models import * 
from ..serializers import *

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        restaurantId = self.request.query_params.get('restaurantId', None)
        owner = self.request.user.profile.owner
        if owner is None:
            return super().get_queryset()
        q1 = super().get_queryset().filter(restaurant__owner=owner)
        if restaurantId is None:
            return q1
        return q1.filter(restaurant__id=restaurantId)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer