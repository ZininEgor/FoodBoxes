from rest_framework.pagination import LimitOffsetPagination


class CartItemPaginator(LimitOffsetPagination):
    limit_query_param = 'limit'
    offset_query_param = 'offset'
