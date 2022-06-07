from django.urls import path
from . import views

urlpatterns = [
    path('updaterecord/', views.updaterecord, name="updaterecord"),
    path('animalrecords/', views.animalrecords, name="animalrecords"),
    path('animalhealth/', views.animalhealth, name="animalhealth"),
    path('breeding/', views.breeding, name="breeding"),
    path('breed_export/', views.export, name="breed-export"),
    path('producesale/', views.producesale, name="producesale"),
    path('farmfinance/', views.farmfinance, name="farmfinance"),
    path('employees/', views.employees, name="employees"),

]
