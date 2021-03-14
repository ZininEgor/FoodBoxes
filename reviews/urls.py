from rest_framework.routers import DefaultRouter

from reviews.views import ReviewViewSet

item_router = DefaultRouter()
item_router.register(r'', ReviewViewSet, basename='review')
urlpatterns = item_router.urls
