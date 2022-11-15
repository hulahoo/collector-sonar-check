from django_filters import rest_framework as filters

from src.models.indicator import Indicator
from src.models.feed import Feed


class IndicatorFilter(filters.FilterSet):
    class Meta:
        model = Indicator
        fields = Indicator.get_model_fields()


class FeedFilter(filters.FilterSet):
    class Meta:
        model = Feed
        fields = Feed.get_model_fields()
        exclude = ['sertificate']
