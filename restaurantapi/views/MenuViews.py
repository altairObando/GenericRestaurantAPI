from rest_framework import generics, validators
from ..models import Menu, MenuCategories, MenuPrices
from ..serializers import MenuSerializer, MenuCategoriesSerializer, MenuPricesSerializer

class MenuList(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class =  MenuSerializer

    def get_queryset(self):
        ownerId = self.request.ownerId
        if ownerId is None or ownerId == '':
            raise validators.ValidationError({'ownerId': 'This field is required.'})
        restaurantId = self.request.query_params.get('restaurantId', None)
        q1 = super().get_queryset().filter(restaurant__owner__id=ownerId)
        if restaurantId is None or restaurantId =='':
            return q1
        return q1.filter(restaurant__id=restaurantId)
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
        return super().get_queryset().filter(menu__id=menuId)
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
        return super().get_queryset().filter(menu__id=menuId)
class MenuPriceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuPrices.objects.all()
    serializer_class = MenuPricesSerializer