from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.http import JsonResponse
from django.core.cache import cache
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from app.users.schemas import UserCreateSchema, UserUpdateSchema, UserListSchema, CustomerCreateSchema, \
    CustomerUpdateSchema, CustomerListSchema
from app.users.serializers import UserSerializer, CustomerSerializer
from app.users.controllers import UserController, CustomerController
from rest_framework.pagination import PageNumberPagination
from app.utils.constants import Timeouts, CacheKeys
from app.utils.helpers import qdict_to_dict, build_cache_key
from app.utils.views import BaseViewSet


class UserViewSet(BaseViewSet):
    # permission_classes = (IsOrganizationUser,)
    controller = UserController()
    serializer = UserSerializer
    create_schema = UserCreateSchema
    update_schema = UserUpdateSchema
    list_schema = UserListSchema
    cache_key_retrieve = CacheKeys.USER_DETAILS_BY_PK
    cache_key_list = CacheKeys.USER_LIST

    @extend_schema(
        description="Create a new user",
        request=UserCreateSchema,
        examples=[
            OpenApiExample('User Creation Request JSON', value={
                "name": "John Doe",
                "mobile_no": "1234567890",
                "role": "admin",
                "director_id": 1
            })
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing user",
        request=UserUpdateSchema,
        examples=[
            OpenApiExample('User Update Request JSON', value={
                "name": "Jane Doe",
                "mobile_no": "0987654321",
                "role": "user",
                "director_id": 2
            })
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List and filter users",
        parameters=[
            OpenApiParameter(name='name', location=OpenApiParameter.QUERY, required=False, type=str,
                             description='name'),
            OpenApiParameter(name='mobile_no', location=OpenApiParameter.QUERY, required=False, type=str,
                             description='mobile_no'),
            OpenApiParameter(name='role', location=OpenApiParameter.QUERY, required=False, type=str,
                             description='role'),
        ],
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific user by id",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='pk'),
        ],
    )
    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        description="Make a user inactive",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='pk'),
        ],
    )
    @action(methods=['POST'], detail=True)
    def make_inactive(self, request, pk, *args, **kwargs):
        return super().make_inactive(request, pk, *args, **kwargs)


class CustomerViewSet(BaseViewSet):
    # permission_classes = (IsOrganizationUser,)
    controller = CustomerController()
    serializer = CustomerSerializer
    create_schema = CustomerCreateSchema
    update_schema = CustomerUpdateSchema
    list_schema = CustomerListSchema
    cache_key_retrieve = CacheKeys.CUSTOMER_DETAILS_BY_PK
    cache_key_list = CacheKeys.CUSTOMER_LIST

    @extend_schema(
        description="Create a new customer",
        request=CustomerCreateSchema,
        responses={201: CustomerSerializer},
        examples=[
            OpenApiExample('Customer Creation Request JSON', value={
                "name": "John Doe",
                "email": "john@example.com",
                "mobile_number": "1234567890",
                "occupation": "Developer",
                "preferences": {"area_of_purpose": [1, 2], "property_types": [1, 3]}
            })
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Retrieve a specific customer by id",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int,
                             description='Customer ID'),
        ],
        responses={200: CustomerSerializer}
    )
    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing customer",
        request=CustomerUpdateSchema,
        responses={200: CustomerSerializer},
        examples=[
            OpenApiExample('Customer Update Request JSON', value={
                "name": "Jane Doe",
                "email": "jane@example.com",
                "mobile_number": "0987654321",
                "occupation": "Manager",
                "preferences": {"area_of_purpose": [3, 4], "property_types": [2, 5]}
            })
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List and filter customers",
        responses={200: CustomerSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='name', type=str),
            OpenApiParameter(name='email', type=str),
            OpenApiParameter(name='mobile_number', type=str),
        ]
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Make a customer inactive",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int,
                             description='Customer ID'),
        ]
    )
    @action(detail=True, methods=['post'])
    def make_inactive(self, request, pk, *args, **kwargs):
        return super().make_inactive(request, pk, *args, **kwargs)
