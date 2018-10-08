from django.contrib import admin
from authors.apps.profiles.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    
    fields = ('user','bio', 'image') 

    list_display = ('user', 'bio','created_at','updated_at')
    
admin.site.register(Profile, ProfileAdmin)