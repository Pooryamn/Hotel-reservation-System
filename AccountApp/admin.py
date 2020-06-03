from django.contrib import admin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','phone','national_id']

admin.site.register(Profile,ProfileAdmin)