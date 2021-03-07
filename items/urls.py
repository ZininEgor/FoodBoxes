from rest_framework.routers import DefaultRouter

from .views import ItemViewSet

item_router = DefaultRouter()
item_router.register(r'', ItemViewSet, basename='item')
urlpatterns = item_router.urls
