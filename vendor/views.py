from django.shortcuts import render,get_object_or_404, redirect
from .forms import vendorForm
from accounts.forms import Vendfor_Profile_Form
from accounts.models import UserProfile
from .models import Vendor
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_vendor_role
from menu.models import Category, FoodItem
from menu.forms import Category_forms
from django.template.defaultfilters import slugify




def get_vendor(request):
    vendor=Vendor.objects.get(vendor_user=request.user)
    return vendor
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


def menue_builder(request):
    vendor = Vendor.objects.get(vendor_user=request.user)
    categories = Category.objects.filter(vendor=vendor).order_by('category_name')
    contex={
        'categories':categories
    }
    return render(request, 'vendor/menue_builder.html', contex)



def food_items_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    foodItems=FoodItem.objects.filter(vendor=vendor, category=category)
    context={
        'foodItems':foodItems,
        'category': category,
    }
    return render(request,'vendor/food_items_by_categories.html',context )

def add_category(request):
    if request.method=='POST':
        form = Category_forms(request.POST)
        if form.is_valid():
            category_name=form.cleaned_data['category_name']
            category=form.save(commit=False)
            category.vendor=get_vendor(request)
            category.slug=slugify(category_name)
            form.save()
            return redirect('menue_builder')
        else:
            form = Category_forms()

    form = Category_forms()
    context={
        'form':form,
    }
    return render(request,'vendor/add_category.html',context)


def edit_category(request,pk=None):
    category = get_object_or_404(Category, pk=pk)

    if request.method=='POST':
        form = Category_forms(request.POST, instance=category)
        if form.is_valid():
            category_name= form.cleaned_data['category_name']
            category= form.save(commit=False)
            category.vendor= get_vendor(request)
            category.slug= slugify(category_name)
            form.save()
            return redirect('menue_builder')
        else:
            print(form.errors)
    else:
        form = Category_forms(instance=category)

    context={
        'form':form,
        'category':category,
        
    }

    return render(request, 'vendor/edit_category.html', context)



def delete_category(request, pk=None):
    category= get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('menue_builder')