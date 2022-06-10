from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser
from . utils import *

# Create your models here.

class User(AbstractUser):
    first_name = last_name = None

    def __str__(self):
        return str(self.username)


# class FoodCategory(models.Model):
#     name = models.CharField(max_length=200, null=True)
#     slug = models.SlugField(max_length=1000, null=True, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.name)

#     class Meta:
#         verbose_name_plural = "Food Categories"

# def food_category_slug_generator(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)

# pre_save.connect(food_category_slug_generator, sender=FoodCategory)

class FoodProduct(models.Model):
    categories = [
        ('Vegetables', 'Vegetables'),
        ('Fruits', 'Fruits'),
        ('Food Stuffs', 'Food Stuffs'),
        ('Meat', 'Meat'),
    ]
    name = models.CharField(max_length=300, null=True)
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    price = models.IntegerField(null=True)
    category = models.CharField(max_length=100, null=True, choices=categories)
    image = models.ImageField(null=True)

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return str(self.name)

def food_slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(food_slug_generator, sender=FoodProduct)


class ShippingAddress(models.Model):
    countries = [
        ('Nigeria', 'Nigeria'),
        ('Ghana', 'Ghana'),
        ('South Africa', 'South Africa'),
        ('Kenya', 'Kenya'),
        ('Togo', 'Togo')
    ]
    name = models.CharField(max_length=1000, null=True)
    email = models.EmailField(max_length=1000, null=True)
    address = models.CharField(max_length=1000, null=True)
    city = models.CharField(max_length=200, null=True)
    zipcode = models.IntegerField(null=True)
    country = models.CharField(max_length=200, choices=countries)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}'s shipping details"

    class Meta:
        verbose_name_plural = 'Shipping Details'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, blank=True, null=True)
    verified = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shipping_address.name}'s order"

    @property
    def get_cart_total(self):
        orderitems = self.orderitems.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitems.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(FoodProduct, on_delete=models.CASCADE, null=True, related_name='products')
    order = models.ForeignKey(Order, related_name='orderitems', null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default="1", null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)    
    def __str__(self):
        return str(self.product.name)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class Message(models.Model):
    name = models.CharField(max_length=1000, null=True)
    phone = models.CharField(max_length= 15, null=True)
    email = models.EmailField(max_length=1000, null=True, blank=True)
    message = models.TextField(null=True)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)