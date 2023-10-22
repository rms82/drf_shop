from django.shortcuts import get_object_or_404, reverse

from rest_framework import serializers

from .models import Post, Comment
from accounts.models import ProfileUser


class PostCommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.user.username")

    class Meta:
        model = Comment
        fields = ["user", "body", "rating"]


class ListPostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.user.username")

    class Meta:
        model = Post
        fields = ["pk", "title", "slug", "image", "author"]
        read_only_fields = [
            "slug",
        ]


class PostSerializer(serializers.ModelSerializer):
    comments = PostCommentSerializer(many=True, read_only=True)
    number_of_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "pk",
            "title",
            "slug",
            "image",
            "author",
            "body",
            "created_at",
            "updated_at",
            "number_of_comments",
            "comments",
        ]
        read_only_fields = [
            "slug",
            "author",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        author = get_object_or_404(ProfileUser, user=request.user)

        return Post.objects.create(author=author, **validated_data)

    def get_number_of_comments(self, post):
        return post.comments.count()


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "body"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["pk", "user", "body", "rating"]

    def create(self, validated_data):
        post_id = self.context.get('post_id')
        user_id = self.context.get('user_id')
        user_profile = get_object_or_404(ProfileUser, user_id=user_id)
        
        return Comment.objects.create(post_id = post_id, user=user_profile, **validated_data)


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["body", "rating"]
