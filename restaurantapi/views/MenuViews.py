from rest_framework import generics, validators
from ..models import Menu, MenuCategories, MenuPrices
from ..serializers import MenuSerializer, MenuCategoriesSerializer, MenuPricesSerializer

class MenuList(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class =  MenuSerializer

    def get_queryset(self):
        restaurantId = self.request.query_params.get('restaurantId', None)
        if restaurantId is None or restaurantId =='':
            raise validators.ValidationError({'restaurantId': 'This field is required'})
        return super().get_queryset().filter(restaurant_id=restaurantId)
class MenuDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuCategoryList(generics.ListCreateAPIView):
    queryset = MenuCategories.objects.all()
    serializer_class =  MenuCategoriesSerializer

    def get_queryset(self):
        menuId = self.request.query_params.get('menuId', None)
        if menuId is None or menuId =='':
            raise validators.ValidationError({'menuId': 'This field is required'})
        return super().get_queryset().filter(menu_id=menuId)
class MenuCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuCategories.objects.all()
    serializer_class = MenuCategoriesSerializer

class MenuPriceList(generics.ListCreateAPIView):
    queryset = MenuPrices.objects.all()
    serializer_class =  MenuPricesSerializer

    def get_queryset(self):
        menuId = self.request.query_params.get('menuId', None)
        if menuId is None or menuId =='':
            raise validators.ValidationError({'menuId': 'This field is required'})
        return super().get_queryset().filter(menu_id=menuId)
class MenuPriceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuPrices.objects.all()
    serializer_class = MenuPricesSerializer