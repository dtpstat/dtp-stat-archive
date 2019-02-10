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
    name = serializers.CharField(source="participant_type")
    color = serializers.SerializerMethodField()

    class Meta:
        model = MVC
        fields = (
            "id",
            "name",
            "color",
            # "region",
            # "alias",
            "datetime",
            # "address",
            # "street",
            # "type",
            "participant_type",
            "lng",
            "lat",
            # "conditions",
            # "dead",
            # "injured",
            # "participants",
            # "scheme",
            # "nearby",
            # "source_data",
            # "geo_updated",
            # "created_at",
        )

    def get_color(self, obj):
        if obj.participant_type.name == "auto":
            return "#FFCA68"
        elif obj.participant_type.name == "bicycle":
            return "#97CA98"
        elif obj.participant_type.name == "pedestrian":
            return "#96CBFE"


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
