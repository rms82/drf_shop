from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404, reverse

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from mail_templated import EmailMessage
from rest_framework_nested import routers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError, DecodeError 
import jwt

from .models import ProfileUser, CustomUser
from .emails import EmailThread
from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomUserSerializer,
    ProfileForUserSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
    ChangePasswordSerializer,
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


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class EmailActivationView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])

        except DecodeError:
            return Response("Invalid Token!")

        except ExpiredSignatureError:
            return Response("Token is expired!")

        except InvalidSignatureError:
            return Response("Invalid Token!")

        user_id = token.get("user_id")
        user = get_object_or_404(CustomUser, pk=user_id)

        if user.is_verify == True:
            return Response("user is already verified")

        user.is_verify = True
        user.save()

        return Response("user is verified now!")


class RegisterView(GenericAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save()
            email = serializer.validated_data.get("email")
            token = self.get_token_for_user(email)

            email_obj = EmailMessage(
                "email/active_user.tpl",
                {"token": token, "url": reverse("email", kwargs={"token": token})},
                "from@example.com",
                to=[f"{email}"],
            )

            EmailThread(email_obj=email_obj).start()

        data = {"detail": "user created! activation link send to your email!"}
        return Response(data, status=status.HTTP_201_CREATED)

    def get_token_for_user(self, email):
        user = get_object_or_404(CustomUser, email=email)
        token = RefreshToken.for_user(user)

        return str(token.access_token)


class ChangePasswordView(GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.user_obj = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get("old_password")
        new_password = serializer.validated_data.get("new_password")

        if not self.user_obj.check_password(old_password):
            return Response(
                {"old_password": "user password is not correct"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.user_obj.set_password(new_password)
        self.user_obj.save()

        return Response({"detail": "password changed!!"})
