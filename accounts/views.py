from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages, auth
from vendor.forms import vendorForm
from .utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

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

            mail_subject='Active your Account'
            email_template='accounts/email/active_account.html'
            send_verification_email(request,user,mail_subject,email_template)

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

            mail_subject='Active your Account'
            email_template='accounts/email/active_account.html'
            send_verification_email(request,user,mail_subject,email_template)


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



def activate(request, uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(User.DoesNotExist, OverflowError, TypeError, ValueError):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Account verify succesfully')
        return redirect('myaccount')
    else:
        messages.error(request,'Invalid Activetion code')
        return redirect(request,'myaccount')


def forget_password(request):
    if request.method=='POST':
        email=request.POST['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)

            mail_subject='Reset Your password'
            email_template='accounts/email/reset_password.html'

            send_verification_email(request, user,mail_subject,email_template)

            messages.success(request, " Send a link to your email")
            return redirect('login')
        else:
            messages.error(request, " User Not found")
            return redirect('login')

        
    return render(request, 'accounts/forget_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except(User.DoesNotExist,TypeError,OverflowError,ValueError):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.info(request,'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request,'This link has been expired')
        return redirect('myaccount')




def reset_password(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            pk=request.session.get('uid')
            user=User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active=True
            user.save()
            messages.success(request,'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request,'Password doesnt match')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')


