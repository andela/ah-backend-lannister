from django.contrib import admin
from authors.apps.authentication.models import User

class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'email','is_active','is_verified','is_staff')
    list_display = ('username', 'email','is_active','is_verified','is_staff')

admin.site.register(User,UserAdmin)