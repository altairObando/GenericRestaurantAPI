from rest_framework import viewsets
from ..filters import RestaurantFilter
from ..models import Restaurant
from ..serializers import RestaurantSerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filterset_class = RestaurantFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        owner = self.request.user.profile.owner
        if owner:
            queryset = queryset.filter(owner=owner)
        return queryset
