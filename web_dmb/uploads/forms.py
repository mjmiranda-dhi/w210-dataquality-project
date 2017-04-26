from django import forms

class DocumentForm(forms.Form):
    file = forms.FileField(label='Select a file')
