from . import models

ROLE_AUTO = 1
ROLE_PEDESTRIAN = 2
ROLE_BICYCLE = 3


def participant_type_id_by_role_text(text):
    text = text.lower()
    if text == 'водитель' or text == 'пассажир':
        return ROLE_AUTO
    elif text == 'велосипедист':
        return ROLE_BICYCLE
    else:
        return ROLE_PEDESTRIAN


def is_injured_status(status):
    normalized_status = status.lower()
    return 'раненый' in normalized_status and 'к категории раненый не относится' not in normalized_status


def is_dead_status(status):
    return 'скончался' in status.lower()


def get_mvcs_by_region(region_alias, area_alias=None):
    if area_alias is None:
        region = models.Region.objects.get(alias=region_alias)
        mvcs_filtered = models.MVC.objects.filter(region__parent_region_id=region.id)
        participant_offences_filtered = models.Participant.objects.filter(mvc__region__parent_region_id=region.id)
    else:
        region = models.Region.objects.get(parent_region__alias=region_alias, alias=area_alias)
        mvcs_filtered = models.MVC.objects.filter(region_id=region.id)
        participant_offences_filtered = models.Participant.objects.filter(mvc__region_id=region.id)

    mvcs = mvcs_filtered.values(
        'id', 'alias', 'datetime', 'address', 'street', 'type_id',
        'longitude', 'latitude', 'dead', 'injured', 'participant_type_id', 'conditions',
    )

    nearyby_objects = mvcs_filtered.values('id', 'nearby__id')

    participant_offences = participant_offences_filtered.values(
        'id', 'mvc__id', 'role', 'status', 'offences__id'
    )

    participants_by_mvcs = {}
    for participant_offence in participant_offences:
        participants = participants_by_mvcs.setdefault(participant_offence['mvc__id'], {})
        participant = participants.get(participant_offence['id'])
        if participant:
            participant['offences'].append(participant_offence['offences__id'])
        else:
            offence_id = participant_offence['offences__id']
            offences = [offence_id] if offence_id is not None else []
            participant = {
                'offences': offences,
                'role': participant_type_id_by_role_text(participant_offence['role']),
                'injured': is_injured_status(participant_offence['status']),
                'dead': is_dead_status(participant_offence['status']),
            }
            participants[participant_offence['id']] = participant

    nearby_by_mvcs = {}
    for nearby in nearyby_objects:
        nearby_for_mvc = nearby_by_mvcs.setdefault(nearby['id'], [])
        nearby_for_mvc.append(nearby['nearby__id'])

    for mvc in mvcs:
        participant_list = []
        participants = participants_by_mvcs.get(mvc['id'])
        if participants:
            participant_list.extend(participants.values())
        mvc['participants'] = participant_list

        mvc['datetime'] = mvc['datetime'].isoformat()

        mvc['nearby'] = nearby_by_mvcs.get(mvc['id'], [])

    return mvcs


def search_region(name_part):
    regions = models.Region.objects.select_related('parent_region').filter(name__icontains=name_part).values(
        'id', 'name', 'alias', 'parent_region__name', 'parent_region__alias'
    ).order_by('name', 'parent_region__name')

    result = []
    for region in regions:
        name = region['name']
        if region.get('parent_region__name') is not None:
            name += ' (' + region.get('parent_region__name') + ')'

        alias = region['alias']
        if region.get('parent_region__alias') is not None:
            alias = region.get('parent_region__alias') + '_' + alias

        result.append({
            'name': name,
            'alias': alias
        })

    return result
