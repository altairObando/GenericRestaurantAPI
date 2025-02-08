from rest_framework import generics, validators
from ..models import * 
from ..serializers import *


class LocationList(generics.ListCreateAPIView):
    queryset = RestaurantLocations.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        owner = self.request.query_params.get('owner', None)
        if owner is None or owner == '':
            raise validators.ValidationError({'owner': 'This field is required.'})
        return super().get_queryset().filter(restaurant__owner=owner)

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantLocations.objects.all()
    serializer_class = LocationSerializer