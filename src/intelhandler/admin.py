from django.contrib import admin
from src.models.indicator import Indicator, Tag
from src.models.feed import Feed

admin.site.register(Indicator)
admin.site.register(Feed)
admin.site.register(Tag)
