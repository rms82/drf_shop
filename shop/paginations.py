from rest_framework.pagination import PageNumberPagination

class ProductPaginate(PageNumberPagination):
    page_size = 50