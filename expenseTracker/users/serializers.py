from .models import CustomUser, UserInfo
from rest_framework import serializers

class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserInfo
        fields = [
            'profile_pic',
            'mobile_number'
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    #nested
    user_info = UserInfoSerializer(required=False)

    class Meta:
        model = CustomUser
        fields= [
            'first_name',
            'last_name',
            'email',
            'password',
            'last_login',
            'user_info'
        ]


    def create(self, validated_data):
        user_info_data = validated_data.pop('user_info', None)
        password = validated_data.pop('password')

        # Create user
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()

        # Create user_info if provided
        if user_info_data:
            UserInfo.objects.create(user=user, **user_info_data)

        return user



    def update(self, instance, validated_data):
        user_info_data = validated_data.pop('user_info', None)

        # Update CustomUser fields
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        # Update or create related UserInfo
        if user_info_data:
            user_info = getattr(instance, 'user_info', None)
            if user_info:
                for attr, value in user_info_data.items():
                    setattr(user_info, attr, value)
                user_info.save()
            else:
                UserInfo.objects.create(user=instance, **user_info_data)

        return instance

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user
    


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()