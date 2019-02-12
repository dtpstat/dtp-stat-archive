from django.db.models import Q, Sum, Case, When
from django.db import models
from rest_framework import viewsets
from rest_framework.response import Response

from dtpmapapp.models import (
    MVC,
    Car,
    MVCParticipantType,
    MVCType,
    Nearby,
    Offence,
    Participant,
    Region,
    Street,
    UpdateLog,
)

from .filters import MVCFilter
from .serializers import (
    CarSerializer,
    MVCParticipantTypeSerializer,
    MVCSerializer,
    MVCTypeSerializer,
    NearbySerializer,
    OffenceSerializer,
    ParticipantSerializer,
    RegionSerializer,
    StreetSerializer,
)


class MVCViewSet(viewsets.ModelViewSet):
    queryset = MVC.objects.select_related("participant_type").all()
    serializer_class = MVCSerializer
    filterset_class = MVCFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset()
            .only("id", "datetime", "participant_type", "lng", "lat")
            .values("id", "datetime", "participant_type", "lng", "lat")
        )

        # serializer = self.get_serializer(queryset, many=True)
        aggregate = queryset.aggregate(
            dead=models.Sum("dead"),
            dead_auto=models.Sum(
                "dead", filter=models.Q(participant_type__name="auto")
            ),
            dead_bicycle=models.Sum(
                "dead", filter=models.Q(participant_type__name="bicycle")
            ),
            dead_pedestrian=models.Sum(
                "dead", filter=models.Q(participant_type__name="pedestrian")
            ),
            injured=models.Sum("injured"),
            injured_auto=models.Sum(
                "injured", filter=models.Q(participant_type__name="auto")
            ),
            injured_bicycle=models.Sum(
                "injured", filter=models.Q(participant_type__name="bicycle")
            ),
            injured_pedestrian=models.Sum(
                "injured", filter=models.Q(participant_type__name="pedestrian")
            ),
        )
        annotate = queryset.annotate(
            color=models.Case(
                models.When(
                    participant_type__name="auto", then=models.Value("#FFCA68")
                ),
                models.When(
                    participant_type__name="bicycle", then=models.Value("#97CA98")
                ),
                models.When(
                    participant_type__name="pedestrian", then=models.Value("#96CBFE")
                ),
                default=models.Value("#000000"),
                output_field=models.CharField(),
            )
        )
        center = None
        if 'ne_lat' not in request.query_params and 'ne_lng' not in request.query_params and 'sw_lat' not in request.query_params and 'sw_lng' not in request.query_params:
            center = {'lat': 54.19, 'lng': 45.18}
        if "region_name" in request.query_params:
            try:
                region = Region.objects.get(name__iexact=request.query_params["region_name"])
            except Region.DoesNotExist:
                region = None
            center = {'lat': region.latitude, 'lng': region.longitude} if region else None
        elif "parent_region_name" in request.query_params:
            try:
                region = Region.objects.get(name__iexact=request.query_params["parent_region_name"])
            except Region.DoesNotExist:
                region = None
            center = {'lat': region.latitude, 'lng': region.longitude} if region else None

        data = {
            "count": queryset.count(),
            "center": center,
            "result": annotate,
            "dead": aggregate["dead"],
            "deadAuto": aggregate["dead_auto"],
            "deadBicycle": aggregate["dead_bicycle"],
            "deadPedestrian": aggregate["dead_pedestrian"],
            "injured": aggregate["injured"],
            "injuredAuto": aggregate["injured_auto"],
            "injuredBicycle": aggregate["injured_bicycle"],
            "injuredPedestrian": aggregate["injured_pedestrian"],
        }
        return Response(data)


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class MVCParticipantTypeViewSet(viewsets.ModelViewSet):
    queryset = MVCParticipantType.objects.all()
    serializer_class = MVCParticipantTypeSerializer


class MVCTypeViewSet(viewsets.ModelViewSet):
    queryset = MVCType.objects.all()
    serializer_class = MVCTypeSerializer


class NearbyViewSet(viewsets.ModelViewSet):
    queryset = Nearby.objects.all()
    serializer_class = NearbySerializer


class OffenceViewSet(viewsets.ModelViewSet):
    queryset = Nearby.objects.all()
    serializer_class = NearbySerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class StreetViewSet(viewsets.ModelViewSet):
    queryset = Street.objects.all()
    serializer_class = StreetSerializer
