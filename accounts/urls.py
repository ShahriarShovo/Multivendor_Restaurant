from django.urls import path
from . import views


urlpatterns=[
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('customerdashboard/', views.customerdashboard, name='customerdashboard'),
    path('vendordashboard/', views.vendordashboard, name='vendordashboard'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forget_password/', views.forget_password, name='forget_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
]