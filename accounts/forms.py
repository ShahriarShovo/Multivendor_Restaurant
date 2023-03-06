from django import forms
from .models import User, UserProfile
from .validator import allow_only_image


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=['fist_name', 'last_name', 'username', 'email','password']
    
    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        password= cleaned_data.get('password')
        confirm_password= cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "Password Does not Match"
            )
        

class Vendfor_Profile_Form(forms.ModelForm):
    profile_picture=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_image])
    cover_photo=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_image])
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'start typing...', 'required': 'required'}))

    #latitude=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    #longitute=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model=UserProfile
        fields=('profile_picture','cover_photo', 'address',
                'country','state','city',
                'pin_code','latitude','longitute',)
        
    def __init__(self, *args, **kwargs):
        super(Vendfor_Profile_Form,self).__init__(*args, **kwargs)
        for field in self.fields:
            if field=='latitude' or field=='longitute':
                self.fields[field].widget.attrs['readonly']='readonly'
            
            
            