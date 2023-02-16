from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages
from vendor.forms import vendorForm

# Create your views here.

def registerUser(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data['password']
            user=form.save(commit=False)
            user.set_password(password)
            user.role=User.CUSTOMER
            user.save()
            messages.success(request, 'You have been register successfully')
            return redirect('registerUser')
        else:
            print(form.errors)
    else:
        form=UserForm()
    context={
        'form':form
    }
    return render(request, 'accounts/registerUser.html',context)


def registerVendor(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        v_form=vendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name=form.cleaned_data['fist_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=User.objects.create_user(fist_name=first_name,
                                          last_name=last_name, email=email,
                                          username=username,password=password)
            user.role=User.VENDOR
            user.save()

            vendor=v_form.save(commit=False)
            vendor.vendor_user=user
            vendor_user_profile=UserProfile.objects.get(user=user)
            vendor.vendor_user_profile=vendor_user_profile
            vendor.save()
            messages.success(request, 'You have been register successfully.Please \
                             wait for approval')
            return redirect('registerVendor')
        else:
            print(form.errors)
            print(v_form.errors)
    else:
        form=UserForm()
        v_form=vendorForm()
    context={
        'form':form,
        'v_form':v_form
    }
    return render(request, 'accounts/registerVendor.html', context)
