from rest_framework import viewsets

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
    MVCParticipantTypeSerializer,
    MVCSerializer,
    MVCTypeSerializer,
    NearbySerializer,
    OffenceSerializer,
    StreetSerializer,
)


class MVCViewSet(viewsets.ModelViewSet):
    queryset = MVC.objects.all()
    serializer_class = MVCSerializer


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


class StreetViewSet(viewsets.ModelViewSet):
    queryset = Street.object.all()
    serializer_class = StreetSerializer
