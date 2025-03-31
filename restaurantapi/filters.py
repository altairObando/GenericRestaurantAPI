from django_filters import rest_framework as filters
from .models import Restaurant

class RestaurantFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name='product__productprice__price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='product__productprice__price', lookup_expr='lte')
    tags = filters.CharFilter(method='filter_tags')

    def filter_tags(self, queryset, name, value):
        tags = value.split(',')
        return queryset.filter(tags__contains=tags)

    class Meta:
        model = Restaurant
        fields = ['name', 'tags', 'owner']