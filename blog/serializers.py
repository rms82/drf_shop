from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import Post, Comment
from accounts.models import ProfileUser


class ListPostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.user.username")

    class Meta:
        model = Post
        fields = ["pk", "title", "slug", "image", "author"]
        read_only_fields = [
            "slug",
        ]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "slug", "image", "author", "body"]
        read_only_fields = ["slug", "author",]

    def create(self, validated_data):
        request = self.context.get("request")
        author = get_object_or_404(ProfileUser, user=request.user)

        return Post.objects.create(author=author, **validated_data)


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "body"]
