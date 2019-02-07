from rest_framework import serializers

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


class MVCSerializer(serializers.ModelSerializer):
    class Meta:
        model = MVC
        fields = (
            "id",
            "region",
            "alias",
            "datetime",
            "address",
            "street",
            "type",
            "participant_type",
            "longitude",
            "latitude",
            "conditions",
            "dead",
            "injured",
            "participants",
            "scheme",
            "nearby",
            "source_data",
            "geo_updated",
            "created_at",
        )


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ("id", "brand", "car_model", "color", "manufacture_year")


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
