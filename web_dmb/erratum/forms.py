from django.contrib.auth.models import User
from django import forms


class signUpForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['email', 'password']


class DocumentForm(forms.Form):
    file = forms.FileField(label='Select a file')