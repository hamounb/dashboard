from django import forms
from .models import *


class FileUploadForm(forms.ModelForm):

    class Meta:
        model = FileModel
        fields = ["date", "category", "file"]