from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse

from app.properties.controllers import PropertyController, PhaseController, PlotController
from app.properties.schemas import PropertyUpdateSchema, PropertyCreateSchema, PropertyListSchema, PhaseCreateSchema, \
    PhaseUpdateSchema, PhaseListSchema, PlotCreateSchema, PlotUpdateSchema, PlotListSchema
from app.properties.serializers import PropertySerializer, PhaseSerializer, PlotSerializer
from app.utils.constants import CacheKeys
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
            OpenApiExample('Property Creation Request JSON', value={
                "property_type": 1,
                "area_of_purpose": 1,
                "name": "Green Acres",
                "dtcp_details": "DTCP Approved",
                "price": 100000.00,
                "amenities": "Swimming pool, Gym",
                "location": "Downtown",
                "phase_number": 1,
                "created_by_id": 1,
                "director_id": 2,
                "current_lead_id": 3
            })
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing property",
        request=PropertyUpdateSchema,
        responses={200: PropertySerializer},
        examples=[
            OpenApiExample('Property Update Request JSON', value={
                "property_type": 1,
                "area_of_purpose": 1,
                "name": "Blue Lagoon",
                "dtcp_details": "Not applicable",
                "price": 150000.00,
                "amenities": "Parking lot, Security",
                "location": "Uptown",
                "phase_number": 2,
                "created_by_id": 2,
                "director_id": 1,
                "current_lead_id": 4
            })
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List and filter properties",
        parameters=[
            OpenApiParameter(name='property_type', type=int),
            OpenApiParameter(name='area_of_purpose', type=int),
            OpenApiParameter(name='phase_number', type=int),
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
    serializer = PlotSerializer
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
