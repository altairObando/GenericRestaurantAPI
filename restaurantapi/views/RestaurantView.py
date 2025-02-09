from rest_framework import generics
from ..models import *
from ..serializers import RestaurantSerializer


class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        owner = self.request.user.profile.owner
        if owner is None:
            return super().get_queryset()
        return super().get_queryset().filter(owner=owner)


class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
