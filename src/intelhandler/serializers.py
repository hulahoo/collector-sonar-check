from rest_framework import serializers

from src.models.feed import Feed
from src.models.indicator import Indicator
from src.intelhandler.models import Source, LogStatistic


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        exclude = []


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        exclude = []


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        exclude = []


class IndicatorWithFeedsSerializer(serializers.ModelSerializer):
    feeds = FeedSerializer(many=True, read_only=True)

    class Meta:
        model = Indicator
        exclude = []

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('feeds')

        return queryset


class LogStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogStatistic
        exclude = []
