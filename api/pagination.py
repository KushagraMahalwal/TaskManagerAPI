from rest_framework.pagination import PageNumberPagination

class TaskPagination(PageNumberPagination):
    page_size = 1  # Default page size
    page_size_query_param = 'page_size'  # Allow user to override ?page_size=10
    max_page_size = 100  # Optional