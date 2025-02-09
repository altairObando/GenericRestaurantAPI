from rest_framework import generics
from ..models import * 
from ..serializers import *

class PricingList(generics.ListCreateAPIView):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer

    def get_queryset(self):
        owner = self.request.user.profile.owner
        if owner is None:
            return super().get_queryset()
        q1 = super().get_queryset().filter(product__restaurant__owner=owner)
        
        restaurantId = self.request.query_params.get('restaurantId',None)
        productId = self.request.query_params.get('productId',None)
        if restaurantId is not None:
            q1 = q1.filter(product__restaurant__id=restaurantId)
        if productId is not None:
            q1 = q1.filter(product__id=productId)
        return q1

        

class PricingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer

    