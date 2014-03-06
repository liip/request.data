from django import forms
from django.forms import ModelForm
from apps.requests.models import Request, User, Agency

class RequestForm(ModelForm):
    description = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={'placeholder': 'Describe your request in a few sentences.'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'What data would you like to request?'}))
    
    class Meta:
        model = Request
        fields = ['title', 'description', 'agency']

class UserForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your email address'}))

    class Meta:
        model = User
        fields = ['name', 'email']

class AgencyForm(ModelForm):
    a_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Which agency are you asking? (If not found in dropdown.)'}))

    class Meta:
        model = Agency
        fields = ['a_name']
