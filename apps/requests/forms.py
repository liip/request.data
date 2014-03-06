from django import forms
from django.forms import ModelForm
from apps.requests.models import Request, User, Agency

class RequestForm(ModelForm):
    description = forms.CharField(max_length=5000, widget=forms.Textarea)

    class Meta:
        model = Request
        fields = ['title', 'description', 'agency']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']

class AgencyForm(ModelForm):
    class Meta:
        model = Agency
        fields = ['a_name']
