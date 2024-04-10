import random

from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.http import JsonResponse
from django.core.cache import cache
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework.response import Response

from app.users.enums import Role
from app.users.schemas import UserCreateSchema, UserUpdateSchema, UserListSchema, CustomerCreateSchema, \
    CustomerUpdateSchema, CustomerListSchema
from app.users.serializers import UserSerializer, CustomerSerializer
from app.users.controllers import UserController, CustomerController
from rest_framework.pagination import PageNumberPagination

from app.users.tasks import send_sms
from app.utils.constants import Timeouts, CacheKeys, SMS
from app.utils.helpers import qdict_to_dict, build_cache_key, mobile_number_validation_check, generate_random_username
from app.utils.views import BaseViewSet

User = get_user_model()


class OtpLoginViewSet(viewsets.ViewSet):

    @extend_schema(
        description="Generates OTP for the provided mobile number and sends it via SMS.",
        request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample('Example JSON', value={"mobile_no": "1234567890"})
        ]
    )
    @action(methods=["POST"], detail=False)
    def generate(self, request):
        # this api does not need auth token
        # Generate otp, store it in cache, send sms using yellow.ai
        # request_body : {"mobile_no"}

        mobile_no = request.data.get('mobile_no', None)
        mobile_no_valid = mobile_number_validation_check(mobile_no)
        if mobile_no_valid is not None:
            return Response(data={"message": mobile_no_valid}, status=status.HTTP_400_BAD_REQUEST)

        mobile_no = str(mobile_no)

        # static_otp_mobile_numbers = ['9344015965', '8971165979', '7013991532', '9959727836', '1414141414',
        #                              '8858327030']  # can keep the numbers in .env file
        # if mobile_no in static_otp_mobile_numbers:
        #     otp = "111111"
        # else:
        otp = str(random.randint(100000, 999999))
        if settings.DEBUG:
            otp = "111111"
        cache.set("otp_" + mobile_no, otp, timeout=300)
        user = User.objects.filter(mobile_no=mobile_no).first()
        if user is None:
            name = "User"
        else:
            name = user.name or "User"
        message = SMS.OTP_LOGIN_MESSAGE.format(name=name, otp=otp)
        # send_sms_result = send_sms(message=message, number=mobile_no)
        # print(send_sms_result)
        # send_sms_result = send_sms.delay(message=message, number=mobile_no)
        # send_sms.apply_async(args=[message, mobile_no], queue='openai')
        send_sms(message, mobile_no)
        # print(send_sms_result.get(timeout=10))  # Waits up to 10 seconds for the result

        # send_sms.apply_async(
        #     kwargs={'mobile_no': mobile_no, 'message': message})
        return Response(data={"message": "otp generated"}, status=status.HTTP_200_OK)

    @extend_schema(
        description="Resends the OTP to the provided mobile number.",
        request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample('Example JSON', value={"mobile_no": "1234567890"})
        ]
    )
    @action(methods=["POST"], detail=False)
    def resend(self, request):
        # request_body : {"mobile_no"}
        mobile_no = request.data.get('mobile_no', None)
        mobile_no_valid = mobile_number_validation_check(mobile_no)
        if mobile_no_valid is not None:
            return Response(data={"message": mobile_no_valid}, status=status.HTTP_400_BAD_REQUEST)
        mobile_no = str(mobile_no)
        otp = cache.get("otp_" + mobile_no)
        if otp:
            user = User.objects.filter(mobile_no=mobile_no).first()
            if user is None:
                name = "User"
            else:
                name = user.name or "User"
            cache.set("otp_" + mobile_no, otp, timeout=300)
            message = SMS.OTP_LOGIN_MESSAGE.format(name=name, otp=otp)
            send_sms.apply_async(args=[message, mobile_no], queue='openai')
            return Response(data={"message": "resent otp"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "OTP not sent or it is expired"}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Verifies the provided OTP and logs in the user.",
        request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample('Example JSON', value={"mobile_no": "1234567890", "otp": "1234"})
        ]
    )
    @action(methods=["POST"], detail=False)
    def verify(self, request):
        # this api does not need auth token
        # request_body : {"otp", "mobile_no"}

        mobile_no = request.data.get('mobile_no', None)
        mobile_no_valid = mobile_number_validation_check(mobile_no)
        if mobile_no_valid is not None:
            return Response(data={"message": mobile_no_valid}, status=status.HTTP_400_BAD_REQUEST)
        mobile_no = str(mobile_no)
        otp = str(request.data.get("otp"))
        otp_from_cache = cache.get("otp_" + mobile_no)
        if otp_from_cache is None:
            return Response(data={"message": "OTP not sent or it is expired"},
                            status=status.HTTP_400_BAD_REQUEST)
        if otp != otp_from_cache:
            return Response(data={"message": "Incorrect otp"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            cache.delete("otp_" + mobile_no)
            user = User.objects.filter(mobile_no=mobile_no).select_related('auth_token').order_by('-id').first()
            if user is None:
                user = User.objects.create(username=generate_random_username())
                user.mobile_no = mobile_no
                token, created = Token.objects.get_or_create(user=user)
                user.auth_token = token
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print(request.user)
            user.last_login = timezone.now()
            user.save()
            auth_token = user.auth_token
            response = Response(data={
                "message": "successfully logged in",
                "user": UserSerializer(user).data,
                "customer": CustomerSerializer(user.customer).data if user.customer else None,
                "token": auth_token.key},
                status=status.HTTP_200_OK)
            return response

    @extend_schema(
        description="Logs out the authenticated user.",
        responses={200: OpenApiTypes.OBJECT}
    )
    @action(methods=["POST"], detail=False)
    def logout(self, request):
        # Get the token associated with the user and delete it
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass  # No token found for user

        logout(request)
        response = Response(data={"message": "successfully logged out"},
                            status=status.HTTP_200_OK)
        return response


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
                "name": "Siva Prakash",
                "email": "siva0109228@gmail.com",
                "mobile_no": "9344015566",
                "occupation": "Developer",
                "address": "16 a VSA LANE",
                "preferences": {"area_of_purpose": [1, 2], "property_types": [1, 3], "budget": 100000}
            })
        ]
    )
    def create(self, request, *args, **kwargs):
        # return super().create(request, *args, **kwargs)

        errors, data = self.controller.parse_request(self.create_schema, request.data)
        if errors:
            return JsonResponse(data=errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                user = User.objects.create(
                    username=generate_random_username(),
                    name=data.name,
                    email=data.email,
                    mobile_no=data.mobile_no,
                    role=Role.CUSTOMER,
                )
                token, created = Token.objects.get_or_create(user=user)
                user.auth_token = token
                user.save()
                errors, instance = self.controller.create(**data.dict(), user=user)
                if errors:
                    return JsonResponse(data=errors, status=status.HTTP_400_BAD_REQUEST)
                return JsonResponse(data={"customer_id": instance.pk, "user_id": user.pk}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)

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
                "name": "Siva Prakash",
                "email": "siva0109228@gmail.com",
                "mobile_no": "9344015566",
                "occupation": "Developer",
                "address": "16 a VSA LANE",
                "preferences": {"area_of_purpose": [1, 2], "property_types": [1, 3], "budget": 100000}
            })
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        # try:
        #     user = User.objects.get(pk=pk)
        #     pk = user.customer.id
        # except ObjectDoesNotExist:
        #     return JsonResponse({'error': 'User not found'}, status=404)
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List and filter customers",
        responses={200: CustomerSerializer(many=True)},
        parameters=[
            OpenApiParameter(name='user_id', type=int),
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
