from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import ProfileUser, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            "pk",
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password_confirm",
        ]

    def validate(self, attrs):
        data = super().validate(attrs)
        password = data.get("password")
        password_confirm = data.get("password_confirm")
        email = data.get("email")

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "user with this email already exits!"})

        if password != password_confirm:
            raise serializers.ValidationError({"password": "passwords does not match!"})

        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        return CustomUser.objects.create_user(**validated_data)


class CustomUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["pk", "username", "is_verify"]


class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserProfileSerializer(read_only=True)

    class Meta:
        model = ProfileUser
        fields = ["pk", "user", "birth_date", "fullname"]


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = [
            "birth_date",
        ]


class ProfileForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ["user", "birth_date", "fullname"]
        read_only_fileds = ["user"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_verify:
            raise serializers.ValidationError({"detail": "User is not verify!"})

        data["user_id"] = self.user.pk

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        data = super().validate(attrs)

        new_password = data.get("new_password")
        new_password_confirm = data.get("new_password_confirm")

        if new_password != new_password_confirm:
            raise serializers.ValidationError({"new_password": "passwords does not match!"})

        try:
            validate_password(new_password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return data

