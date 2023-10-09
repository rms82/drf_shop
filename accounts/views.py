from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from rest_framework_nested import routers

from .models import ProfileUser
from .serializers import (
    ProfileSerializer,
    UpdateProfileSerializer,
    ProfileForUserSerializer,
)


# Create your views here.
class ProfileViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "put", "delete", "head", "options"]
    serializer_class = ProfileSerializer
    queryset = ProfileUser.objects.all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return UpdateProfileSerializer

        return ProfileSerializer

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = self.request.user
        profile = get_object_or_404(ProfileUser, user=user)

        if request.method == "GET":
            serializer = ProfileForUserSerializer(profile)

            return Response(serializer.data)

        elif request.method == "PUT":
            serializer = ProfileForUserSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)
