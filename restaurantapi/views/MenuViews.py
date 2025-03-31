from rest_framework import viewsets, filters
from ..models import Menu, MenuCategories, MenuPrices
from ..serializers import MenuSerializer, MenuCategoriesSerializer, MenuPricesSerializer

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        owner = self.request.user.profile.owner
        if owner:
            queryset = queryset.filter(restaurant__owner=owner)
            restaurant_id = self.request.query_params.get('restaurantId')
            if restaurant_id:
                queryset = queryset.filter(restaurant_id=restaurant_id)
        return queryset

class MenuCategoryViewSet(viewsets.ModelViewSet):
    queryset = MenuCategories.objects.all()
    serializer_class = MenuCategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        owner = self.request.user.profile.owner
        if owner:
            queryset = queryset.filter(menu__restaurant__owner=owner)
            menu_id = self.request.query_params.get('menuId')
            if menu_id:
                queryset = queryset.filter(menu_id=menu_id)
        return queryset

class MenuPriceViewSet(viewsets.ModelViewSet):
    queryset = MenuPrices.objects.all()
    serializer_class = MenuPricesSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price']

    def get_queryset(self):
        queryset = super().get_queryset()
        owner = self.request.user.profile.owner
        if owner:
            queryset = queryset.filter(menu__restaurant__owner=owner)
            menu_id = self.request.query_params.get('menuId')
            if menu_id:
                queryset = queryset.filter(menu_id=menu_id)
        return queryset