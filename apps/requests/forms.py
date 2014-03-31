from django import forms
from django.forms import ModelForm
from apps.requests.models import Request, User, Agency, Comment

class RequestForm(ModelForm):
    description = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={'placeholder': 'Describe your request in a few sentences'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'What data would you like to request?'}))
    agency = forms.ModelChoiceField(queryset=Agency.objects.all(), empty_label="Select an agency")

    class Meta:
        model = Request
        fields = ['title', 'description', 'agency']

class UserForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your email address'}))

class AgencyForm(ModelForm):
    a_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Or specify another agency'}))

    class Meta:
        model = Agency
        fields = ['a_name']

class CommentForm(ModelForm):
    description = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={'placeholder': 'Leave a comment on this request'}))

    class Meta:
        model = Comment
        fields = ['description']
