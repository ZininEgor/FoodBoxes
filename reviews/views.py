from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from reviews import serializers
from reviews.models import Review
from reviews.paginators import ReviewPaginator


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Review.objects.all()
    pagination_class = ReviewPaginator
    authentication_classes = [TokenAuthentication]
    serializer_class = serializers.ReviewSerializer
    permission_classes_by_action = {
        'list': [AllowAny],
        'create': [IsAuthenticated]
    }

    def get_queryset(self):
        queryset = Review.objects.filter(status=Review.StatusReview.PUBLISHED)
        return queryset

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]
