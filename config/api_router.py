from django.conf import settings
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter, SimpleRouter

from app.crm.views import CRMLeadViewSet, StatusChangeRequestViewSet, PaymentViewSet, SiteVisitViewSet
from app.properties.views import PropertyViewSet, PlotViewSet, PhaseViewSet
from app.users.views import UserViewSet, CustomerViewSet, OtpLoginViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet, basename="users")
router.register("otp", OtpLoginViewSet, basename='otp')
router.register("customers", CustomerViewSet, basename="customers")
router.register("properties", PropertyViewSet, basename="properties")
router.register("phases", PhaseViewSet, basename="phases")
router.register("plots", PlotViewSet, basename="plots")
router.register("crm-leads", CRMLeadViewSet, basename="crm-leads")
router.register("status-change-requests", StatusChangeRequestViewSet, basename="status-change-requests")
router.register("payments", PaymentViewSet, basename="payments")
router.register("site-visits", SiteVisitViewSet, basename="site-visits")

app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    # path('get-enum-values/', get_enum_values, name='get_enum_values'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),
]
