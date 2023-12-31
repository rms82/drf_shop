from django.db.models import Prefetch

from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import (
    DjangoModelPermissions,
    IsAdminUser,
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response


from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Comment, Category, Like
from .pagination import PostPaginate, PostCommentPaginate
from .permissions import (
    CommentIsOwnerOrAdminOrReadOnly,
    IsAdminOrReadOnly,
    IsOwnerOrAdminOrReadOnly,
)
from .serializers import (
    PostSerializer,
    ListPostSerializer,
    UpdatePostSerializer,
    CommentSerializer,
    UpdateCommentSerializer,
    BlogCategorySerializer,
    BlogUpdateCategorySerializer,
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
        return Post.objects.select_related("author__user").prefetch_related(
            Prefetch("comments", queryset=Comment.objects.select_related("user__user")),
            "category",
        )

    def get_permissions(self):
        if self.request.method == "POST":
            return [
                IsAuthenticated(),
            ]

        return [
            IsOwnerOrAdminOrReadOnly(),
        ]

    def get_serializer_context(self):
        return {"request": self.request}


class PostCommentViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    pagination_class = PostCommentPaginate
    filter_backends = [OrderingFilter]
    ordering_fields = ["updated_at"]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateCommentSerializer

        return CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.select_related("post", "user__user")
        post_id = self.kwargs.get("post_pk")

        return queryset.filter(post_id=post_id)

    def get_permissions(self):
        if self.request.method == "POST":
            return [
                IsAuthenticated(),
            ]
        return [CommentIsOwnerOrAdminOrReadOnly()]

    def get_serializer_context(self):
        return {
            "post_id": self.kwargs.get("post_pk"),
            "user_id": self.request.user.pk,
        }


class CategoryViewSet(viewsets.ModelViewSet):
    filter_backends = [OrderingFilter]
    ordering_fields = ["name", "created_at"]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return BlogUpdateCategorySerializer

        return BlogCategorySerializer

    def get_queryset(self):
        return Category.objects.select_related("parent").prefetch_related("subcategory")

    def get_permissions(self):
        return [IsAdminOrReadOnly()]


class LikeView(GenericAPIView):
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        user_id = request.user.pk

        try:
            post = Post.objects.get(pk=pk)
            like_obj = Like.objects.get(user_id=user_id, post_id=pk)
            like_obj.delete()
            return Response("dislike", status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        except Like.DoesNotExist:
            like_obj = Like.objects.create(post_id=pk, user_id=user_id)

            return Response('liked', status=status.HTTP_200_OK)
