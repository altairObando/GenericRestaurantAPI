from rest_framework import generics
from ..models import * 
from ..serializers import *

class PricingList(generics.ListCreateAPIView):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer

class PricingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer