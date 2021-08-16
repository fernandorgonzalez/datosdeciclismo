from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import actividades
from .models import atletas

admin.site.register(actividades)
admin.site.register(atletas)
