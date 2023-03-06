from django.shortcuts import render,get_object_or_404, redirect
from .forms import vendorForm
from accounts.forms import Vendfor_Profile_Form
from accounts.models import UserProfile
from .models import Vendor
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_vendor_role

# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def vprofile(request):
    profile=get_object_or_404(UserProfile, user=request.user)
    vendor_profile=get_object_or_404(Vendor, vendor_user=request.user)

    if request.method=='POST':
        profile_form=Vendfor_Profile_Form(request.POST, request.FILES, instance=profile)
        vendor_form=vendorForm(request.POST, request.FILES, instance=vendor_profile)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            return redirect('vprofile')
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form=Vendfor_Profile_Form(instance=profile)
        vendor_form=vendorForm(instance=vendor_profile)
    context={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'profile':profile,
        'vendor_profile':vendor_profile,
    }
    return render(request, 'vendor/vprofile.html',context)