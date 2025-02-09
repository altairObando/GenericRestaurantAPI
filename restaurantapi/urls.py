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
]