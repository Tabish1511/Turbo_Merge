from django import forms
from .models import PDFDoc




class PDFForm(forms.ModelForm):

    class Meta:
        model = PDFDoc
        fields = ['upload', 'custom_integer']
        labels = {'upload': '', 'custom_integer':''}
