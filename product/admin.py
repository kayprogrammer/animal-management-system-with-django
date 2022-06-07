from django.contrib import admin
from . models import *
# Register your models here.

myModels = [User, FoodProduct, ShippingAddress, Order, OrderItem, Message] 

admin.site.register(myModels)