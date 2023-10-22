from rest_framework.pagination import PageNumberPagination

class PostPaginate(PageNumberPagination):
    page_size = 20

class PostCommentPaginate(PageNumberPagination):
    page_size = 10