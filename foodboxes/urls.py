from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='Stepic DRF API',
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

apipatterns = [
    path('items/', include(('items.urls', 'items'), namespace='items')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('reviews/', include(('reviews.urls', 'reviews'), namespace='reviews')),
    path('order/', include(('orders.urls', 'orders'), namespace='orders')),
    path('carts/', include(('carts.urls', 'carts'), namespace='carts')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),  # noqa
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(apipatterns)),
]
