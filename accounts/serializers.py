from rest_framework import serializers

from .models import ProfileUser, CustomUser


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
        fields = ["birth_date",]
    

class ProfileForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ["user", "birth_date", "fullname"]
        read_only_fileds = ['user']
    