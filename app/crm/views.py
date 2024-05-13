from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse

from app.crm.controllers import CRMLeadController, StatusChangeRequestController, PaymentController, SiteVisitController
from app.crm.schemas import CRMLeadCreateSchema, CRMLeadUpdateSchema, CRMLeadListSchema, \
    StatusChangeRequestCreateSchema, StatusChangeRequestUpdateSchema, StatusChangeRequestListSchema, \
    PaymentCreateSchema, PaymentUpdateSchema, PaymentListSchema, SiteVisitCreateSchema, SiteVisitUpdateSchema, \
    SiteVisitListSchema
from app.crm.serializers import CRMLeadSerializer, StatusChangeRequestSerializer, PaymentSerializer, SiteVisitSerializer
from app.properties.controllers import PropertyController, PhaseController, PlotController
from app.properties.schemas import PropertyUpdateSchema, PropertyCreateSchema, PropertyListSchema, PhaseCreateSchema, \
    PhaseUpdateSchema, PhaseListSchema, PlotCreateSchema, PlotUpdateSchema, PlotListSchema
from app.properties.serializers import PropertySerializer, PhaseSerializer, PlotSerializer
from app.utils.constants import CacheKeys
from app.utils.views import BaseViewSet


class CRMLeadViewSet(BaseViewSet):
    controller = CRMLeadController()  # Replace with your actual controller
    serializer = CRMLeadSerializer  # Replace with your actual serializer
    create_schema = CRMLeadCreateSchema
    update_schema = CRMLeadUpdateSchema
    list_schema = CRMLeadListSchema
    cache_key_retrieve = CacheKeys.CRM_LEAD_DETAILS_BY_PK  # Update as needed
    cache_key_list = CacheKeys.CRM_LEAD_LIST  # Update as needed

    @extend_schema(
        description="Create a new CRM lead",
        request=CRMLeadCreateSchema,
        responses={201: CRMLeadSerializer},
        examples=[
            OpenApiExample('CRM Lead Creation Request JSON', value={
                "property_id": 1,
                "customer_id": 2,
                "assigned_so": 3,
                "details": {
                    "property_name": "",
                    "property_type": 1,
                    "phase_no": 1,
                    "plot_no": 2,
                    "sq_ft": 2000,
                    "is_corner": True
                },
                "current_status": 1
            })
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing CRM lead",
        request=CRMLeadUpdateSchema,
        responses={200: CRMLeadSerializer},
        examples=[
            OpenApiExample('CRM Lead Update Request JSON', value={
                "property_id": 1,
                "customer_id": 2,
                "assigned_so": 3,
                "details": {
                    "property_name": "",
                    "property_type": 1,
                    "phase_no": 1,
                    "plot_no": 2,
                    "sq_ft": 2000,
                    "is_corner": True
                },
                "current_status": 1
            })
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List and filter CRM leads",
        parameters=[
            OpenApiParameter(name='property_id', type=int),
            OpenApiParameter(name='customer_id', type=int),
            OpenApiParameter(name='assigned_so_id', type=int),
            OpenApiParameter(name='current_status', type=int),
        ],
        responses={200: CRMLeadSerializer(many=True)}
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific CRM lead by id",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='CRM '
                                                                                                             'Lead ID'),
        ],
        responses={200: CRMLeadSerializer}
    )
    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    @extend_schema(
        description="Make a CRM lead inactive",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='CRM '
                                                                                                             'Lead ID'),
        ],
        responses={200: OpenApiResponse(description="CRM lead inactivated successfully")}
    )
    @action(methods=['POST'], detail=True)
    def make_inactive(self, request, pk, *args, **kwargs):
        return super().make_inactive(request, pk, *args, **kwargs)


class StatusChangeRequestViewSet(BaseViewSet):
    controller = StatusChangeRequestController()
    serializer = StatusChangeRequestSerializer
    create_schema = StatusChangeRequestCreateSchema
    update_schema = StatusChangeRequestUpdateSchema
    list_schema = StatusChangeRequestListSchema
    cache_key_retrieve = CacheKeys.STATUS_CHANGE_REQUEST_DETAILS_BY_PK
    cache_key_list = CacheKeys.STATUS_CHANGE_REQUEST_LIST

    @extend_schema(
        description="Create a new status change request",
        request=StatusChangeRequestCreateSchema,
        responses={201: StatusChangeRequestSerializer},
        examples=[
            OpenApiExample('Status Change Request Creation JSON', value={
                "crm_lead_id": 1,
                "requested_by_id": 2,
                "actioned_by_id": 3,
                "requested_status": 1,
                "approval_status": 1,
                "date_approved": "2023-01-01T00:00:00Z",
                "date_rejected": "2023-01-01T00:00:00Z",
            })
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing status change request",
        request=StatusChangeRequestUpdateSchema,
        responses={200: StatusChangeRequestSerializer},
        examples=[
            OpenApiExample('Status Change Request Update JSON', value={
                "crm_lead_id": 1,
                "requested_by_id": 2,
                "actioned_by_id": 3,
                "requested_status": 1,
                "approval_status": 1,
                "date_approved": "2023-01-01T00:00:00Z",
                "date_rejected": "2023-01-01T00:00:00Z",
            })
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List and filter status change requests",
        parameters=[
            OpenApiParameter(name='crm_lead_id', type=int),
            OpenApiParameter(name='requested_by_id', type=int),
            OpenApiParameter(name='actioned_by_id', type=int),
            OpenApiParameter(name='requested_status', type=int),
            OpenApiParameter(name='approval_status', type=int),
            # Include other parameters as needed
        ],
        responses={200: StatusChangeRequestSerializer(many=True)}
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific status change request by id",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int,
                             description='Status Change Request ID'),
        ],
        responses={200: StatusChangeRequestSerializer}
    )
    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class PaymentViewSet(BaseViewSet):
    controller = PaymentController()  # Replace with actual controller
    serializer = PaymentSerializer  # Replace with actual serializer
    create_schema = PaymentCreateSchema
    update_schema = PaymentUpdateSchema
    list_schema = PaymentListSchema
    cache_key_retrieve = CacheKeys.PAYMENT_DETAILS_BY_PK  # Update as needed
    cache_key_list = CacheKeys.PAYMENT_LIST  # Update as needed

    @extend_schema(
        description="Create a new payment",
        request=PaymentCreateSchema,
        responses={201: PaymentSerializer},
        examples=[
            OpenApiExample('Payment Creation Request JSON', value={
                "crm_lead_id": 1,
                "amount": 10000.00,
                "payment_mode": 1,
                "payment_status": 1,
                "payment_date": "2023-01-01T00:00:00Z",
                "payment_for": 1,
                "payment_detail": "Initial deposit",
                "reference_number": "REF12345"
            })
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing payment",
        request=PaymentUpdateSchema,
        responses={200: PaymentSerializer},
        examples=[
            OpenApiExample('Payment Update Request JSON', value={
                "crm_lead_id": 1,
                "amount": 5000.00,
                "payment_mode": 1,
                "payment_status": 1,
                "payment_date": "2023-01-02T00:00:00Z",
                "payment_for": 1,
                "payment_detail": "First installment",
                "reference_number": "REF67890"
            })
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List and filter payments",
        parameters=[
            OpenApiParameter(name='crm_lead_id', type=int),
            OpenApiParameter(name='payment_mode', type=int),
            OpenApiParameter(name='payment_status', type=int),
            OpenApiParameter(name='payment_for', type=int),
            OpenApiParameter(name='start_time', type=str),
            OpenApiParameter(name='end_time', type=str)
            # Include other parameters as needed
        ],
        responses={200: PaymentSerializer(many=True)}
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific payment by id",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int,
                             description='Payment ID'),
        ],
        responses={200: PaymentSerializer}
    )
    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)


class SiteVisitViewSet(BaseViewSet):
    controller = SiteVisitController()  # Replace with actual controller
    serializer = SiteVisitSerializer  # Replace with actual serializer
    create_schema = SiteVisitCreateSchema
    update_schema = SiteVisitUpdateSchema
    list_schema = SiteVisitListSchema
    cache_key_retrieve = CacheKeys.SITE_VISIT_DETAILS_BY_PK  # Update as needed
    cache_key_list = CacheKeys.SITE_VISIT_LIST  # Update as needed

    @extend_schema(
        description="Create a new site visit",
        request=SiteVisitCreateSchema,
        responses={201: SiteVisitSerializer},
        examples=[
            OpenApiExample('Site Visit Creation Request JSON', value={
                "crm_lead_id": 1,
                "is_pickup": True,
                "pickup_address": "123 Main St",
                "pickup_date": "2023-01-01T00:00:00Z",
                "is_drop": True,
                "drop_address": "456 Elm St",
                "feedback": "Very informative visit"
            })
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description="Partially update an existing site visit",
        request=SiteVisitUpdateSchema,
        responses={200: SiteVisitSerializer},
        examples=[
            OpenApiExample('Site Visit Update Request JSON', value={
                "crm_lead_id": 1,
                "is_pickup": False,
                "pickup_address": "23113f dasda ",
                "pickup_date": "2023-01-01T00:00:00Z",
                "is_drop": False,
                "drop_address": "asd dsad",
                "feedback": "Changed feedback"
            })
        ]
    )
    def partial_update(self, request, pk, *args, **kwargs):
        return super().partial_update(request, pk, *args, **kwargs)

    @extend_schema(
        description="List and filter site visits",
        parameters=[
            OpenApiParameter(name='crm_lead_id', type=int),
            OpenApiParameter(name='is_pickup', type=bool),
            OpenApiParameter(name='pickup_date', type=str),
            OpenApiParameter(name='is_drop', type=bool)
            # Include other parameters as needed
        ],
        responses={200: SiteVisitSerializer(many=True)}
    )
    def list(self, request, **kwargs):
        return super().list(request, **kwargs)

    @extend_schema(
        description="Retrieve a specific site visit by id",
        parameters=[
            OpenApiParameter(name='pk', location=OpenApiParameter.PATH, required=True, type=int, description='Site Visit ID'),
        ],
        responses={200: SiteVisitSerializer}
    )
    def retrieve(self, request, pk, *args, **kwargs):
        return super().retrieve(request, pk, *args, **kwargs)

    # Define 'make_inactive' or other custom actions if required
