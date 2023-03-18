from django import forms
from .models import Category

class Category_forms(forms.ModelForm):
    class Meta:
        model= Category
        fields=['category_name','description']

