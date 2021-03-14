from rest_framework.routers import DefaultRouter

from orders.views import OrderViewSet

item_router = DefaultRouter()
item_router.register(r'', OrderViewSet, basename='order')
urlpatterns = item_router.urls
