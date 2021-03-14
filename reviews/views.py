from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from reviews.models import Review
from reviews.paginators import ReviewPaginator
from reviews.serializers import ReviewSerializer


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Review.objects.all()
    pagination_class = ReviewPaginator
    serializer_class = ReviewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes_by_action = {
        'list': [AllowAny],
        'create': [IsAuthenticated]
    }

    def get_queryset(self):
        queryset = Review.objects.filter(status='published')
        return queryset

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]
