from rest_framework import generics
from ..models import * 
from ..serializers import *

class OrderList(generics.ListAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

    def get_queryset(self):
        owner = self.request.user.profile.owner
        if owner is None:
            return super().get_queryset()
        q1 = super().get_queryset().filter(restaurant__owner=owner)
        restaurantId = self.request.query_params.get('restaurantId', None)
        if restaurantId is None or restaurantId == '':
            return q1
        return q1.filter(restaurant__id=restaurantId)

class OrderListCreate(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


    