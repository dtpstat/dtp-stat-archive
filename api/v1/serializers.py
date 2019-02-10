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
        fields = ("id", "name", "alias")


class MVCParticipantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MVCParticipantType
        fields = ("id", "name", "label", "value")


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = (
            "id",
            "role",
            "offences",
            "driving_experience",
            "status",
            "gender",
            "abscond",
            "mvc",
            "car",
        )


class NearbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nearby
        fields = ("id", "name")


class OffenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offence
        fields = ("id", "name")


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = (
            "id",
            "name",
            "alias",
            "oktmo_code",
            "level",
            "parent_region",
            "status",
            "longitude",
            "latitude",
        )


class StreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = ("id", "name")
