from django import forms
from .models import Vendor
from accounts.validator import allow_only_image


class vendorForm(forms.ModelForm):
    vendor_license=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_image])
    class Meta:
        model=Vendor
        fields=['vendor_name', 'vendor_license']