from rest_framework import generics, validators
from ..models import *
from ..serializers import RestaurantSerializer


class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        owner = self.request.query_params.get('owner', None)
        if owner is None or owner == '':
            raise validators.ValidationError({'owner': 'This field is required.'})
        return super().get_queryset().filter(owner=owner)


class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
