from rest_framework import viewsets, filters
from ..models import Product
from ..serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'category__name']
    ordering_fields = ['name', 'code']

    def get_queryset(self):
        queryset = super().get_queryset()
        owner = self.request.user.profile.owner
        if owner:
            queryset = queryset.filter(restaurant__owner=owner)
            restaurant_id = self.request.query_params.get('restaurantId')
            if restaurant_id:
                queryset = queryset.filter(restaurant_id=restaurant_id)
        return queryset