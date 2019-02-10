import requests
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from dtpmapapp import models
from . import queries
from . import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.cache import cache_page
import user_agents


def home(request):
    return render(request, 'index.html', context={})


def about(request):
    return render(request, 'about.html')


def region(request, region_alias):
    if "_" in region_alias:
        region_alias, area_alias = region_alias.split("_")
        region_item = get_object_or_404(models.Region, alias=area_alias, parent_region__alias=region_alias)
    else:
        region_alias, area_alias = region_alias, None
        region_item = get_object_or_404(models.Region, alias=region_alias)

    user_agent = user_agents.parse(request.META['HTTP_USER_AGENT'])

    if region_item.status or region_item.parent_region.status:
        return render(request, 'area.html', context={
            "region": region_item,
            "region_alias": region_alias,
            "area_alias": repr(area_alias) if area_alias is not None else 'null',
            "is_mobile": user_agent.is_mobile,
        })
    else:
        # Get parent region if exist else current
        region_item = region_item.parent_region or region_item

        return render(request, 'no_area.html', context={
            'region_item': region_item
        })


def mvc(request, mvc_alias):
    mvc = get_object_or_404(models.MVC, alias=mvc_alias)
    cars = models.Car.objects.filter(participant__mvc=mvc).distinct()
    participants = models.Participant.objects.filter(mvc=mvc,car=None)
    offences = [x for x in models.Participant.objects.filter(mvc=mvc).values("offences__name","role") if x['offences__name'] is not None]

    return render(request, 'mvc.html', context={
        "region": mvc.region,
        "mvc": mvc,
        "cars":cars,
        "offences": offences,
        "participants": participants,
        "participant_type_id": mvc.participant_type,
    })


@cache_page(24 * 60 * 60)
@api_view(['GET'])
def mvcs_by_area(request, region_alias, area_alias):
    mvcs = queries.get_mvcs_by_region(region_alias, area_alias)
    return Response(mvcs)


@cache_page(24 * 60 * 60)
@api_view(['GET'])
def mvcs_by_region(request, region_alias):
    mvcs = queries.get_mvcs_by_region(region_alias)
    return Response(mvcs)


@cache_page(24 * 60 * 60)
@api_view(['GET'])
def dicts(request):
    streets = models.Street.objects.all()
    street_serializer = serializers.StreetSerializer(streets, many=True)

    offences = models.Offence.objects.all()
    offence_serializer = serializers.OffenceSerializer(offences, many=True)

    mvc_types = models.MVCType.objects.all()
    mvc_type_serializer = serializers.MVCTypeSerializer(mvc_types, many=True)

    mvc_participant_types = models.MVCParticipantType.objects.all()
    mvc_participant_type_serializer = serializers.MVCParticipantTypeSerializer(mvc_participant_types, many=True)

    nearby = models.Nearby.objects.all()
    nearby_serializer = serializers.NearbySerializer(nearby, many=True)

    return Response({
        'streets': street_serializer.data,
        'offences': offence_serializer.data,
        'mvc_types': mvc_type_serializer.data,
        'mvc_participant_types': mvc_participant_type_serializer.data,
        'nearby': nearby_serializer.data
    })

@api_view(['GET'])
def participant_types(request):
    mvc_participant_types = models.MVCParticipantType.objects.all()
    mvc_participant_type_serializer = serializers.MVCParticipantTypeSerializer(mvc_participant_types, many=True)

    return Response({
        'mvc_participant_types': mvc_participant_type_serializer.data,
    })


@api_view(['GET'])
def search_region(request):
    name_part = request.GET['term']
    if name_part is None or len(name_part) < 2:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    regions = queries.search_region(name_part)
    return Response({'regions': regions})
