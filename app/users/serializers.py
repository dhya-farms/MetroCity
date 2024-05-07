from django.core.validators import RegexValidator
from rest_framework import serializers
from app.users.models import User, Customer
from app.users.enums import Role
from app.utils.helpers import get_serialized_enum


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Role.choices)
    director = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'mobile_no', 'role', 'created_at', 'updated_at', 'director', 'email',
                  'is_active', 'last_login', 'date_joined']

    def get_role(self, obj):
        if obj.role:
            return get_serialized_enum(Role(obj.role))
        return dict()


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    def get_favorites(self, obj):
        # Simplify the output to avoid deep serialization, if needed
        return [prop.id for prop in obj.favorites.all()]  # Just return a list of property IDs

    class Meta:
        model = Customer
        fields = [
            'id',
            'user',
            'favorites',
            'name',
            'image',
            'mobile_no',
            'email',
            'occupation',
            'preferences',
            'address',
            'created_by',
            'created_at',
            'updated_at'
        ]
