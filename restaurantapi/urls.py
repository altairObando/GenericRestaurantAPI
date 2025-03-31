from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'products', ProductViewSet)
router.register(r'menus', MenuViewSet)
router.register(r'menu-categories', MenuCategoryViewSet)
router.register(r'menu-prices', MenuPriceViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'pricing', PricingViewSet)
router.register(r'owners', OwnerViewSet)
router.register(r'contacts', ContactViewSet)

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile-view'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
]

urlpatterns += router.urls