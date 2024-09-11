from .models import Gallery
from django import forms


class GalleryModelForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ["name", "description"]