from datetime import datetime

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse

from app.properties.controllers import PropertyController, PhaseController, PlotController
from app.properties.schemas import PropertyUpdateSchema, PropertyCreateSchema, PropertyListSchema, PhaseCreateSchema, \
    PhaseUpdateSchema, PhaseListSchema, PlotCreateSchema, PlotUpdateSchema, PlotListSchema
from app.properties.serializers import PropertySerializer, PhaseSerializer, PlotSerializer, PlotSerializerSimple
from app.utils.constants import CacheKeys
from app.utils.pagination import CustomPageNumberPagination
from app.utils.views import BaseViewSet


class PropertyViewSet(BaseViewSet):
    controller = PropertyController()
    serializer = PropertySerializer
    create_schema = PropertyCreateSchema
    update_schema = PropertyUpdateSchema
    list_schema = PropertyListSchema
    cache_key_retrieve = CacheKeys.PROPERTY_DETAILS_BY_PK
    cache_key_list = CacheKeys.PROPERTY_LIST

    @extend_schema(
        description="Create a new property",
        request=PropertyCreateSchema,
        responses={201: PropertySerializer},
        examples=[
            OpenApiExample('Property Creation Request JSON', value=
            {
                "property_type": 1,
                "description": "Luxurious community plots available with full amenities.",
                "area_of_purpose": 1,
                "name": "Sunset Vistas",
                "price": 250000.00,
                "details": {
                    "plots_available": 20,
                    "sq_ft_from": "1500",
                    "dtcp_details": "Approved for construction",
                    "amenities": ["Community Pool", "Jogging Track"],
                    "nearby_attractions": ["Lake View", "Shopping Mall"]
                },
                "location": "Downtown Riverside",
                "gmap_url": "https://maps.google.com/maps?q=123+Main+St+Cityville",
                "director_id": 101,
                "current_lead_id": 205
            }
                           )
        ]
    )
    def create(self, request, *args, **kwargs):
        errors, data = self.controller.parse_request(self.create_schema, request.data)
        if errors:
            return JsonResponse(data=errors, status=status.HTTP_400_BAD_REQUEST)

        errors, instance = self.controller.create(**data.dict(), created_by=request.user)
        if errors:
            return JsonResponse(data=errors, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(data={"id": instance.pk}, status=status.HTTP_201_CREATED)

    @extend_schema(
        description="Partially update an existing property",
        request=PropertyUpdateSchema,
        responses={200: PropertySerializer},
        examples=[
            OpenApiExample('Property Update Request JSON', value=
            {
                "property_type": 1,
                "description": "Luxurious community plots available with full amenities.",
                "area_of_purpose": 1,
                "name": "Sunset Vistas",
                "price": 250000.00,
                "details": {
                    "plots_available": 20,
                    "sq_ft_from": "1500",
                    "dtcp_details": "Approved for construction",
                    "amenities": ["Community Pool", "Jogging Track"],
                    "nearby_attractions": ["Lake View", "Shopping Mall"]
                },
                "location": "Downtown Riverside",
                "gmap_url": "https://maps.google.com/maps?q=123+Main+St+Cityville",
                "director_id": 101,
                "current_lead_id": 205
            }
            )
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List and filter properties",
        parameters=[
            OpenApiParameter(name='property_type', type=int),
            OpenApiParameter(name='area_of_purpose', type=int),
            OpenApiParameter(name='created_by_id', type=int),
            OpenApiParameter(name='director_id', type=int),
            OpenApiParameter(name='current_lead_id', type=int),
            OpenApiParameter(name='start_time', type=datetime),
            OpenApiParameter(name='end_time', type=datetime),
        ],
        responses={200: PropertySerializer(many=True)}
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific property by id",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='Property ID'),
        ],
        responses={200: PropertySerializer}
    )
    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        description="Make a property inactive",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='Property ID'),
        ],
        responses={200: OpenApiResponse(description="Property inactivated successfully")}
    )
    @action(methods=['POST'], detail=True)
    def make_inactive(self, request, pk, *args, **kwargs):
        return super().make_inactive(request, pk, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='add-to-favorites')
    def add_to_favorites(self, request, pk=None):
        customer = request.user.customer
        property = self.controller.get_instance_by_pk(pk=pk)
        if not property:
            return JsonResponse({"error": "Property with this ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        customer.favorites.add(property)
        return JsonResponse({'status': 'property added to favorites'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='remove-from-favorites')
    def remove_from_favorites(self, request, pk=None):
        customer = request.user.customer
        property = self.controller.get_instance_by_pk(pk=pk)
        if not property:
            return JsonResponse({"error": "Property with this ID does not exist"}, status=status.HTTP_404_NOT_FOUND)
        customer.favorites.remove(property)
        return JsonResponse({'status': 'property removed from favorites'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='my-favourites')
    def list_favorites(self, request):
        paginator = CustomPageNumberPagination()
        customer = request.user.customer
        queryset = customer.favorites.all()
        page = paginator.paginate_queryset(queryset, request, view=self)
        if page is not None:
            res = self.controller.serialize_queryset(page, self.serializer)
            return paginator.get_paginated_response(res)
        res = self.controller.serialize_queryset(queryset, self.serializer)
        return JsonResponse(res, safe=False, status=status.HTTP_200_OK)


class PhaseViewSet(BaseViewSet):
    controller = PhaseController()
    serializer = PhaseSerializer
    create_schema = PhaseCreateSchema
    update_schema = PhaseUpdateSchema
    list_schema = PhaseListSchema
    cache_key_retrieve = CacheKeys.PHASE_DETAILS_BY_PK
    cache_key_list = CacheKeys.PHASE_LIST

    @extend_schema(
        description="Create a new phase",
        request=PhaseCreateSchema,
        responses={201: PhaseSerializer},
        examples=[
            OpenApiExample('Phase Creation Request JSON', value={
                "property_id": 1,
                "phase_number": 1,
                "description": "Initial phase",
                "start_date": "2023-01-01T00:00:00Z",
                "estimated_completion_date": "2023-12-31T00:00:00Z",
                "status": "planning"
            })
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing phase",
        request=PhaseUpdateSchema,
        responses={200: PhaseSerializer},
        examples=[
            OpenApiExample('Phase Update Request JSON', value={
                "phase_number": 2,
                "description": "Second phase",
                "start_date": "2024-01-01T00:00:00Z",
                "estimated_completion_date": "2024-12-31T00:00:00Z",
                "status": "in_progress"
            })
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List and filter phases",
        parameters=[
            OpenApiParameter(name='property_id', type=int),
            OpenApiParameter(name='phase_number', type=int),
            OpenApiParameter(name='status', type=str),
        ],
        responses={200: PhaseSerializer(many=True)}
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific phase by id",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='Phase ID'),
        ],
        responses={200: PhaseSerializer}
    )
    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        description="Make a phase inactive",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='Phase ID'),
        ],
        responses={200: OpenApiResponse(description="Phase inactivated successfully")}
    )
    @action(methods=['POST'], detail=True)
    def make_inactive(self, request, pk, *args, **kwargs):
        return super().make_inactive(request, pk, *args, **kwargs)


class PlotViewSet(BaseViewSet):
    controller = PlotController()
    serializer = PlotSerializerSimple
    create_schema = PlotCreateSchema
    update_schema = PlotUpdateSchema
    list_schema = PlotListSchema
    cache_key_retrieve = CacheKeys.PLOT_DETAILS_BY_PK
    cache_key_list = CacheKeys.PLOT_LIST

    @extend_schema(
        description="Create a new plot",
        request=PlotCreateSchema,
        responses={201: PlotSerializer},
        examples=[
            OpenApiExample('Plot Creation Request JSON', value={
                "phase_id": 1,
                "plot_number": 101,
                "is_corner_site": True,
                "dimensions": "30x40",
                "facing": 1,
                "soil_type": 2,
                "plantation": "Mango Trees",
                "price": 50000.00,
                "area_size": 1200,
                "area_size_unit": "SQ_FT",
                "availability": "available"
            })
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing plot",
        request=PlotUpdateSchema,
        responses={200: PlotSerializer},
        examples=[
            OpenApiExample('Plot Update Request JSON', value={
                "phase_id": 1,
                "plot_number": 102,
                "is_corner_site": False,
                "dimensions": "40x60",
                "facing": 1,
                "soil_type": 2,
                "plantation": "Pine Trees",
                "price": 75000.00,
                "area_size": 2400,
                "area_size_unit": "SQ_FT",
                "availability": "sold"
            })
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List and filter plots",
        parameters=[
            OpenApiParameter(name='phase_id', type=int),
            OpenApiParameter(name='is_corner_site', type=bool),
            OpenApiParameter(name='availability', type=int),
            OpenApiParameter(name='facing', type=int),
            OpenApiParameter(name='soil_type', type=int),
        ],
        responses={200: PlotSerializer(many=True)}
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific plot by id",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='Plot ID'),
        ],
        responses={200: PlotSerializer}
    )
    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        description="Make a plot inactive",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='Plot ID'),
        ],
        responses={200: OpenApiResponse(description="Plot inactivated successfully")}
    )
    @action(methods=['POST'], detail=True)
    def make_inactive(self, request, pk, *args, **kwargs):
        return super().make_inactive(request, pk, *args, **kwargs)
