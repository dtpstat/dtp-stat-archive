from rest_framework import serializers

from dtpmapapp.models import MVCParticipantType, MVCType, Nearby, Offence, Street


class MVCTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MVCType
        fields = ("id", "name")


class MVCParticipantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MVCParticipantType
        fields = ("id", "name", "label", "value")


class NearbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nearby
        fields = ("id", "name")


class OffenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offence
        fields = ("id", "name")


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = ("id", "name")

