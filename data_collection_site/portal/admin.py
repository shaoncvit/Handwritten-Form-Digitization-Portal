from django.contrib import admin
from .models import UserProfile, FilledForm

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(FilledForm)
