from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    page_size = 50
    page_query_param = "p"
