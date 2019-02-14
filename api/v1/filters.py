from django.db import models
from django_filters import (
    BaseCSVFilter,
    FilterSet,
    NumberFilter,
    CharFilter,
    DateTimeFromToRangeFilter,
)

from dtpmapapp.models import MVC

class CharArrayFilter(BaseCSVFilter, CharFilter):
     pass


class MVCFilter(FilterSet):
    region = NumberFilter(field_name="region__oktmo_code", lookup_expr="exact")
    region_name = CharFilter(field_name="region__name", lookup_expr="iexact")
    parent_region = NumberFilter(
        field_name="region__parent_region__oktmo_code", lookup_expr="exact"
    )
    parent_region_name = CharFilter(
        field_name="region__parent_region__name", lookup_expr="iexact"
    )

    mvc_type = NumberFilter(field_name="type", lookup_expr="exact")
    mvc_type_string = CharFilter(method="filter_mvc_type_string")

    participant_type = NumberFilter(field_name="participant_type", lookup_expr="exact")
    participant_type_string = CharFilter(method="filter_participant_type_string")

    street = NumberFilter(field_name="street", lookup_expr="exact")
    street_string = CharFilter(field_name="street__name", lookup_expr="icontains")

    datetime = DateTimeFromToRangeFilter(field_name="datetime")

    conditions = CharArrayFilter(field_name="conditions", lookup_expr="overlap")


    ne_lat = NumberFilter(field_name="lat", lookup_expr="lte")
    ne_lng = NumberFilter(field_name="lng", lookup_expr="lte")
    sw_lat = NumberFilter(field_name="lat", lookup_expr="gte")
    sw_lng = NumberFilter(field_name="lng", lookup_expr="gte")

    priority = ("region", "parent_region", "region_name", "parent_region_name")

    class Meta:
        model = MVC
        fields = (
            "region",
            "region_name",
            "parent_region",
            "parent_region_name",
            "mvc_type",
            "mvc_type_string",
            "participant_type",
            "participant_type_string",
            "street",
            "street_string",
            "datetime",
            "conditions",
            "ne_lat",
            "ne_lng",
            "sw_lat",
            "sw_lng",
        )

    def filter_mvc_type_string(self, queryset, name, value):
        return queryset.filter(
            models.Q(name__icontains=value) | models.Q(alias__icontains=value)
        )

    def filter_participant_type_string(self, queryset, name, value):
        return queryset.filter(
            models.Q(name__icontains=value) | models.Q(alias__icontains=value)
        )

    def filter_queryset(self, queryset):
        for name, value in self.form.cleaned_data.items():
            queryset = self.filters[name].filter(queryset, value)
            assert isinstance(queryset, models.QuerySet), (
                "Expected '%s.%s' to return a QuerySet, but got a %s instead."
                % (type(self).__name__, name, type(queryset).__name__)
            )
        return queryset