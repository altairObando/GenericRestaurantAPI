from rest_framework import generics, validators
from ..models import * 
from ..serializers import *

class OrderList(generics.ListAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

    def get_queryset(self):
        ownerId = self.request.ownerId
        restaurantId = self.request.query_params.get('restaurantId', None)
        if ownerId is None or ownerId == '':
            raise validators.ValidationError({'ownerId': 'This field is required.'})
        q1 = super().get_queryset().filter(restaurant__owner__id=ownerId)
        if restaurantId is None or restaurantId == '':
            return q1
        return q1.filter(restaurant__id=restaurantId)

class OrderListCreate(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


    