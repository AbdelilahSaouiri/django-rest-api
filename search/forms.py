from django import forms
from .models import Item

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class FormInput(forms.ModelForm):
    class Meta:
        model=Item
        fields=['name','value']
