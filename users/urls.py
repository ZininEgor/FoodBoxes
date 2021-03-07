from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from users.views import CreateUserView, UserView

authpatterns = [
    path('login/', obtain_auth_token),
    path('register/', CreateUserView.as_view())
]

urlpatterns = [
    path('auth/', include(authpatterns)),
    path('current/', UserView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
    })),
]
