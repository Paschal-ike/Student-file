from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser,Student, Upload

class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = ('username', 'email', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
        ('Groups', {'fields': ('groups',)}),
    )
    
admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Student)
admin.site.register(Upload)