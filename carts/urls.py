from django.urls import path, include
from rest_framework.routers import DefaultRouter

from carts import views

item_router = DefaultRouter()
item_router.register(r'items', views.CartITemViewSet, basename='CartItem')
urlpatterns = [
    path(r'', views.CartViewSet.as_view({
        'get': 'retrieve'
    }), name='cart-list'),
    path('', include(item_router.urls)),
]
