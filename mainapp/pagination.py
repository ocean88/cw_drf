from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Настройки пагинации"""

    page_size = 5
