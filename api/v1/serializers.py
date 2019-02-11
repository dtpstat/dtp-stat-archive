from django.db import models
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


def model_to_dict(inst, nested=[]):
    if inst is None:
        return None
    if not isinstance(inst, models.Model):
        ret = []
        for i in inst.all():
            ret.append(model_to_dict(i, nested))
        return ret
    else:
        obj = {}
        for key, val in inst.__dict__.items():
            if not key.startswith("_"):
                obj[key] = val
        if isinstance(nested, dict):
            for n, v in nested.items():
                obj[n] = model_to_dict(getattr(inst, n), v)
        else:
            for n in nested:
                obj[n] = model_to_dict(getattr(inst, n))
        return obj


class HackSerializer:
    nested = []

    def __init__(self, instance=None, context=None, **kwargs):
        self.data = []
        for i in instance:
            self.data.append(model_to_dict(i, self.nested))
