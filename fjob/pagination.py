from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    """
    Custom pagination class with a default page size of 10.

    Attributes:
    - page_size: The number of items to include on each page.
    - page_query_param: The query parameter to determine the current page.
    """

    page_size = 10
    page_query_param = "p"
