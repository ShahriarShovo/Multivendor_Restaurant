from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages, auth
from vendor.forms import vendorForm
from .utils import detectUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

# Create your views here.
# vendor pass test
def check_vendor_role(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied
    
# customer pass test
def check_customer_role(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied
    

def registerUser(request):
    if request.user.is_authenticated:

        messages.warning(request, 'You are already Loggin')
        return redirect('dashboard')
    elif request.method=='POST':
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
    if request.user.is_authenticated:
        messages.warning(request, 'You are already Loggin')
        return redirect('dashboard')
    elif request.method=='POST':
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


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already Loggin')
        return redirect('dashboard')
    elif request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,'You have logged in Successfully')
            return redirect('myaccount')
        else:
            messages.error(request, 'User not exsist')
            return redirect('login')

        
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'You are logged out')
    return redirect('login')


@login_required(login_url='login')
def myaccount(request):
    user=request.user
    redirectUrl=detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_customer_role)
def customerdashboard(request):
    return render(request,'accounts/customerdashboard.html')

@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def vendordashboard(request):
    return render(request,'accounts/vendordashboard.html')

