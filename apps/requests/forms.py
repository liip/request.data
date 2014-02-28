from django import forms
from django.forms import ModelForm
from apps.requests.models import Request

class RequestForm(ModelForm):
    description = forms.CharField(max_length=5000, widget=forms.Textarea)

    class Meta:
        model = Request
        fields = ["title", "description", "agency", "creator"]

