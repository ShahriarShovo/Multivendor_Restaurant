from django import forms
from .models import Category, FoodItem
from accounts.validator import allow_only_image

class Category_forms(forms.ModelForm):
    class Meta:
        model= Category
        fields=['category_name','description']


class FoodItem_form(forms.ModelForm):
    image=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_image])
    class Meta:
        model=FoodItem
        fields=['category','food_title','description','price','image','is_available']