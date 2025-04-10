from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Restaurant, RestaurantLocations, Menu, MenuCategories
from ..serializers import (
    RestaurantSerializer, 
    LocationSerializer, 
    MenuSerializer,
    MenuCategoriesSerializer,
    UserSerializer
)

class ConfigViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def initial_setup(self, request):
        user = request.user
        profile = user.profile
        
        # Get user's restaurants or assigned location
        if profile.owner:
            restaurants = Restaurant.objects.filter(owner=profile.owner)
            restaurant_data = RestaurantSerializer(restaurants, many=True).data
            locations = RestaurantLocations.objects.filter(restaurant__in=restaurants)
            location_data = LocationSerializer(locations, many=True).data
        else:
            location = profile.active_location
            if location:
                restaurant_data = RestaurantSerializer(location.restaurant).data
                location_data = LocationSerializer([location], many=True).data
            else:
                restaurant_data = []
                location_data = []

        # Get menus for these restaurants
        menus = Menu.objects.filter(restaurant__in=restaurants)
        menu_data = MenuSerializer(menus, many=True).data

        return Response({
            'user': UserSerializer(user).data,
            'role': profile.role,
            'restaurants': restaurant_data,
            'locations': location_data,
            'menus': menu_data,
            'app_settings': {
                'currency': 'USD',
                'tax_rate': 0.13,
                'order_statuses': ['PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'],
                'payment_methods': ['CASH', 'CARD', 'MOBILE'],
                'table_management_enabled': True,
                'reservation_enabled': False
            }
        })

    @action(detail=False, methods=['get'])
    def app_version(self, request):
        return Response({
            'min_version': '1.0.0',
            'latest_version': '1.0.0',
            'force_update': False,
            'update_message': None
        })