from django.core.validators import RegexValidator
from django.db.models import Q
from rest_framework import serializers

from app.crm.enums import PropertyStatus, ApprovalStatus
from app.crm.models import CRMLead
from app.users.models import User, Customer, FAQ, UserQuery
from app.users.enums import Role
from app.utils.helpers import get_serialized_enum


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Role.choices)
    director = serializers.SerializerMethodField()
    clients = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'mobile_no', 'role', 'points', 'created_at', 'updated_at', 'director', 'clients',
                  'address', 'email', 'is_active', 'last_login', 'date_joined']

    def get_director(self, obj):
        if obj.director:
            return {
                "id": obj.director.id,
                "name": obj.director.name
            }
        return None

    def get_clients(self, obj):
        # Check if the user role is SALES_OFFICER
        if obj.role == Role.SALES_OFFICER:
            leads_count = CRMLead.objects.filter(
                assigned_so=obj
            ).exclude(
                Q(current_crm_status=PropertyStatus.DOCUMENT_DELIVERY) |
                Q(current_approval_status=ApprovalStatus.COMPLETED)
            ).count()
            return leads_count
        return None

    def get_role(self, obj):
        if obj.role:
            return get_serialized_enum(Role(obj.role))
        return dict()


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class UserQuerySerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = UserQuery
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    def get_favorites(self, obj):
        # Simplify the output to avoid deep serialization, if needed
        return [phase.id for phase in obj.favorites.all()]  # Just return a list of property IDs

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
