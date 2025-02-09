from rest_framework import generics, validators
from ..models import * 
from ..serializers import *


class LocationList(generics.ListCreateAPIView):
    queryset = RestaurantLocations.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        ownerId = self.request.ownerId
        restaurantId = self.request.query_params.get('restaurantId',None)
        if ownerId is None or ownerId == '':
            raise validators.ValidationError({'ownerId': 'This field is required.'})
        q1 = super().get_queryset().filter(parent=None).filter(restaurant__owner=ownerId)
        if restaurantId is None or ownerId == '':
            return q1
        return q1.filter(restaurant__id=restaurantId)

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantLocations.objects.all()
    serializer_class = LocationSerializer