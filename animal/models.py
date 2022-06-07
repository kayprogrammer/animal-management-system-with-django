from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Animal(models.Model):
    animal_choices = [
        ('Cow', 'Cow'),
        ('Goat', 'Goat'),
        ('Chicken', 'Chicken'),
        ('Rabbit', 'Rabbit'),
        ('Fish', 'Fish'),
        ('Pig', 'Pig'),
        ('Duck', 'Duck')
    ]
    idt = models.IntegerField(unique=True, null=True)
    name = models.CharField(max_length=200, null=True)
    sire_id = models.IntegerField(null=True)
    dam_id = models.IntegerField(null=True)
    animal_type = models.CharField(max_length=200, null=True, choices=animal_choices)
    ear_tag = models.CharField(max_length=200, null=True)
    color = models.CharField(max_length=200, null=True)
    breed = models.CharField(max_length=200, null=True)
    pasture = models.CharField(max_length=200, null=True)
    birth_rate = models.CharField(max_length=200, null=True)
    current_age = models.CharField(max_length=200, null=True)
    weight = models.CharField(max_length=200, null=True)
    first_age = models.CharField(max_length=200, null=True)
    birth_date = models.DateField(default=timezone.now, null=True)

    def __str__(self):
        return str(self.name)

class HealthReport(models.Model):
    animal = models.OneToOneField(Animal, on_delete=models.SET_NULL, related_name="healthreports", null=True)
    type = models.CharField(max_length=200, null=True)
    diagnosis = models.CharField(max_length=1000, null=True)
    treatment = models.CharField(max_length=200, null=True)
    cost = models.CharField(max_length=200, null=True)
    vet = models.CharField(max_length=200, null=True)
    date_created = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.animal)

class Breeding(models.Model):
    bull = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="bullbreedings", null=True)
    calf = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="calfbreedings", null=True)
    pregnancy_diagnosis_date = models.DateField(default=timezone.now)
    breeding_date = models.DateField(default=timezone.now)
    calve_due_date = models.DateField(default=timezone.now)
    calved_date = models.DateField(default=timezone.now)
    calf_notes = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return str(self.bull)

class ClientData(models.Model):
    name = models.CharField(max_length=1000, null=True)
    contact = models.CharField(max_length=1000, null=True)
    amount = models.CharField(max_length=1000, null=True)
    date_bought = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.name)

class Finance(models.Model):
    choices = [
        ('income', 'income'),
        ('expense', 'expense'),
    ]
    type = models.CharField(max_length=200, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date_incurred = models.DateField(default=timezone.now)
    type2 = models.CharField(max_length=20, null=True, choices=choices)


class Employee(models.Model):
    choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    designation_choices = [
        ('Administrator', 'Administrator'),
        ('Regular', 'Regular'),
        ('Employee', 'Employee')
    ]
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    emp_id = models.IntegerField(unique=True, null=True)
    emp_name = models.CharField(max_length=200, null=True)
    dob = models.DateField(default=timezone.now)
    date_hired = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=200, null=True, choices=choices)
    contact = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=200, null=True, choices=designation_choices)
    salary = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    job_title = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.emp_name)
