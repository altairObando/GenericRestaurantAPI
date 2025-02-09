from rest_framework import generics
from ..models import * 
from ..serializers import *


class LocationList(generics.ListCreateAPIView):
    queryset = RestaurantLocations.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        owner = self.request.user.profile.owner
        if owner is None:
            return super().get_queryset()
        restaurantId = self.request.query_params.get('restaurantId',None)
        q1 = super().get_queryset().filter(parent=None).filter(restaurant__owner=owner)
        if restaurantId is None:
            return q1
        return q1.filter(restaurant__id=restaurantId)

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantLocations.objects.all()
    serializer_class = LocationSerializer