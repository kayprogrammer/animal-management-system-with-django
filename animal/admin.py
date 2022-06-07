from django.contrib import admin
from . models import *
# Register your models here.

myModels = [Animal, HealthReport, Finance, Employee, Breeding, ClientData]

admin.site.register(myModels)