from django.contrib import admin

from accounts.models import User, UserProfile
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display=('email', 'username','role','is_active','date_joined')
    ordering=('-date_joined',)
    filter_horizontal=()
    list_filter=()
    fieldsets=() 


admin.site.register(User,CustomUserAdmin)
admin.site.register(UserProfile)
