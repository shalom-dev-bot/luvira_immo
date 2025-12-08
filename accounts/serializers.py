from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import OwnerRequest

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'address', 'cni', 'birth_date', 'gender', 'profile_photo', 'is_verified', 'notifications_enabled', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.role = validated_data.get('role', 'client')
        user.phone = validated_data.get('phone', '')
        user.address = validated_data.get('address', '')
        user.cni = validated_data.get('cni', '')
        user.birth_date = validated_data.get('birth_date')
        user.gender = validated_data.get('gender', '')
        user.profile_photo = validated_data.get('profile_photo')
        user.is_verified = validated_data.get('is_verified', False)
        user.notifications_enabled = validated_data.get('notifications_enabled', True)
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)

class OwnerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerRequest
        fields = ['id', 'user', 'documents', 'status', 'created_at']