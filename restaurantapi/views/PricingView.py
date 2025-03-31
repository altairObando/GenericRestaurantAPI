from rest_framework import viewsets, filters
from ..models import ProductPrice
from ..serializers import ProductPriceSerializer

class PricingViewSet(viewsets.ModelViewSet):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        owner = self.request.user.profile.owner
        if owner:
            queryset = queryset.filter(product__restaurant__owner=owner)
            restaurant_id = self.request.query_params.get('restaurantId')
            product_id = self.request.query_params.get('productId')
            if restaurant_id:
                queryset = queryset.filter(product__restaurant_id=restaurant_id)
            if product_id:
                queryset = queryset.filter(product_id=product_id)
        return queryset

    