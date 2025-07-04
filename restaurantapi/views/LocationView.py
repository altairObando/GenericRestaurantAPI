from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import RestaurantLocations, Orders
from ..serializers import LocationSerializer, OrdersSerializer
from datetime import datetime
class LocationViewSet(viewsets.ModelViewSet):
    queryset = RestaurantLocations.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['location', 'restaurant__name']

    def get_queryset(self):
        queryset = super().get_queryset()
        owner = self.request.user.profile.owner
        if owner:
            queryset = queryset.filter(restaurant__owner=owner)
            restaurant_id = self.request.query_params.get('restaurantId')
            if restaurant_id:
                queryset = queryset.filter(restaurant__id=restaurant_id)
        return queryset

    @action(detail=False, methods=['get'])
    def available_locations(self, request):
        query = self.get_queryset()
        sublocations = query.filter(parent__isnull=False)
        date_filter = request.query_params.get('date')
        if date_filter:
            date_filter = datetime.strptime(date_filter, '%Y-%m-%d').date()
            available = sublocations.exclude(orders__order_status='ACTIVE', orders__created_at__date=date_filter)
            serializer = LocationSerializer(available, many=True)
            return Response(serializer.data)
        
        available = sublocations.exclude(orders__order_status='ACTIVE')
        serializer = LocationSerializer(available, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def active_order(self, request, pk=None):
        order = Orders.objects.filter(location=pk, order_status='ACTIVE').first()
        if not order:
            return Response({'message': 'No active order found'}, status=404)
        serializer = OrdersSerializer(order)
        return Response(serializer.data)