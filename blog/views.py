from django.db.models import Prefetch


from rest_framework import viewsets

from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.permissions import (
    DjangoModelPermissions,
    IsAdminUser,
    AllowAny,
    IsAuthenticated,
)


from django_filters.rest_framework import DjangoFilterBackend


from .models import Post, Comment
from .pagination import PostPaginate

from .permissions import IsOwnerOrAdminOrReadOnly

from .serializers import (
    PostSerializer,
    ListPostSerializer,
    UpdatePostSerializer,
)


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    pagination_class = PostPaginate
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "body"]
    ordering_fields = ["title", "created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return ListPostSerializer
        
        if self.request.method == "PATCH":
            return UpdatePostSerializer

        return PostSerializer

    def get_queryset(self):
        return Post.objects.select_related("author__user")

    def get_permissions(self):
        if self.request.method == "POST":
            return [
                IsAuthenticated(),
            ]

        return [IsOwnerOrAdminOrReadOnly()]

    def get_serializer_context(self):
        return {"request": self.request}
