from rest_framework import viewsets, filters
from ..models import ProductPrice
from ..serializers import ProductPriceSerializer
from datetime import datetime
class PricingViewSet(viewsets.ModelViewSet):
    queryset = ProductPrice.objects.all()
    serializer_class = ProductPriceSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price', 'valid_to']

    def get_queryset(self):
        queryset = super().get_queryset()
        owner = self.request.user.profile.owner
        if owner:
            queryset = queryset.filter(product__restaurant__owner=owner)
            restaurant_id = self.request.query_params.get('restaurantId')
            product_id = self.request.query_params.get('productId')
            product_name = self.request.query_params.get('productName')
            only_valid = self.request.query_params.get('onlyValid')
            if only_valid == 1:
                queryset = queryset.filter(valid_to__isnull=True,valid_to__gte=datetime.now())
            if restaurant_id:
                queryset = queryset.filter(product__restaurant_id=restaurant_id)
            if product_name:
                queryset = queryset.filter(product__name__startswith=product_name)
            if product_id:
                queryset = queryset.filter(product_id=product_id)
        return queryset

    