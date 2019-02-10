from rest_framework import viewsets
from rest_framework.response import Response

from django.db.models import Q, Sum

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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset().only("id", "datetime", "participant_type", "lng", "lat")
        )
        serializer = self.get_serializer(queryset, many=True)
        aggregate = queryset.aggregate(
            dead=Sum("dead"),
            dead_auto=Sum("dead", filter=Q(participant_type__name="auto")),
            dead_bicycle=Sum("dead", filter=Q(participant_type__name="bicycle")),
            dead_pedestrian=Sum("dead", filter=Q(participant_type__name="pedestrian")),
            injured=Sum("injured"),
            injured_auto=Sum("injured", filter=Q(participant_type__name="auto")),
            injured_bicycle=Sum("injured", filter=Q(participant_type__name="bicycle")),
            injured_pedestrian=Sum(
                "injured", filter=Q(participant_type__name="pedestrian")
            ),
        )

        data = {
            "count": queryset.count(),
            "result": serializer.data,
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
