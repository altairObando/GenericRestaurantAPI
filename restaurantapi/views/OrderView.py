from rest_framework import generics
from ..models import * 
from ..serializers import *

class OrderList(generics.ListAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

class OrderListCreate(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


    