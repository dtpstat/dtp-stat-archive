from rest_framework import serializers
from . import models


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Street
        fields = ['id', 'name']


class OffenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Offence
        fields = ['id', 'name']


class MVCTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MVCType
        fields = ['id', 'name']


class MVCParticipantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MVCParticipantType
        fields = ['id', 'name', 'label', 'value']


class NearbySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Nearby
        fields = ['id', 'name']
