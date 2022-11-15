from django import forms

from src.models.feed import Feed


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        exclude = ["indicators", "parsing_rules"]
