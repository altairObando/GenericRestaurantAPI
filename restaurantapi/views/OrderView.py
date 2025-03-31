from rest_framework import viewsets, filters
from ..models import Orders
from ..serializers import OrdersSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['order_number', 'customer__name']
    ordering_fields = ['created_at', 'order_status']

    def get_queryset(self):
        queryset = super().get_queryset()
        owner = self.request.user.profile.owner
        if owner:
            queryset = queryset.filter(location__restaurant__owner=owner)
            location_id = self.request.query_params.get('locationId')
            if location_id:
                queryset = queryset.filter(location_id=location_id)
        return queryset


    