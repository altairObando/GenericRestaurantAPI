from django.urls import path
from .views import *


urlpatterns = [
    path('contacts/', ContactList.as_view(), name='contact-list'),
    path('contacts/<int:pk>/', ContactDetail.as_view(), name='contact-detail'),
    path('restaurants/', RestaurantList.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', RestaurantDetail.as_view(), name='restaurant-detail'),
    path('locations/', LocationList.as_view(), name='location-list'),
    path('locations/<int:pk>/', LocationDetail.as_view(), name='location-detail'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('pricing/', PricingList.as_view(), name='pricing-list'),
    path('pricing/<int:pk>/', PricingDetail.as_view(), name='pricing-detail'),
    path('menu/', MenuViews.MenuList.as_view(), name='menu-list'),
    path('menu/<int:pk>/', MenuViews.MenuDetail.as_view(), name='menu-detail'),
    path('menucategory/', MenuViews.MenuCategoryList.as_view(), name='menu-category-list'),
    path('menucategory/<int:pk>/', MenuViews.MenuCategoryDetail.as_view(), name='menu-category-detail'),
    path('menuprice/', MenuViews.MenuPriceList.as_view(), name='menu-price-list'),
    path('menuprice/<int:pk>/', MenuViews.MenuPriceDetail.as_view(), name='menu-price-detail'),
    path('profile/', ProfileView.as_view(), name='profile-view')
]