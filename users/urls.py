from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from users.views import CreateUserView, UserViewSet

authpatterns = [
    path('login/', obtain_auth_token),
    path('register/', CreateUserView.as_view(), name='register')
]

urlpatterns = [
    path('auth/', include(authpatterns)),
    path('current/', UserViewSet.as_view(), name='current'),
]
