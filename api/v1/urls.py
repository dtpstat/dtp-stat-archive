from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import (
    MVCParticipantTypeViewSet,
    MVCTypeViewSet,
    NearbyViewSet,
    OffenceViewSet,
    StreetViewSet,
)

router = DefaultRouter()
router.register(
    r"mvc-participant-types",
    MVCParticipantTypeViewSet,
    basename="mvc-participant-types",
)
router.register(r"mvc-types", MVCTypeViewSet, basename="mvc-types")
router.register(r"nearby", NearbyViewSet, basename="nearby")
router.register(r"offences", OffenceViewSet, basename="offences")
router.register(r"streets", StreetViewSet, basename="streets")


schema_view = get_schema_view(
    openapi.Info(
        title="DTP stat API",
        default_version="v1",
        description="Routes of DTP stat project",
    ),
    # validators=['flex', 'ssv'],
    public=False,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "swagger(<str:format>.json|.yaml)", schema_view.without_ui(), name="schema-json"
    ),
    path("swagger/", schema_view.with_ui("swagger"), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc"), name="schema-redoc"),
    path("", include((router.urls, "api-root")), name="api-root"),
]
