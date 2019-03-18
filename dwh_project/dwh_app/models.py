'''	This file contains the different classes of django model; this is effectively an abstraction layer that will interact with the sqlite database.
	Each class will be represented as a table; with its attribute being the table fields.
'''
from django.db import models

# Create your models here.

class Person(models.Model):
    ''' Person class identifies a unique physical person by its first name, last name and email '''
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)
    first_name         = models.CharField(max_length=100)
    last_name          = models.CharField(max_length=100)
    email              = models.CharField(max_length=100)
    
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Vehicle(models.Model):
    ''' Vehicle class uniquely with the registration plate number '''
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)
    registration_plate = models.CharField(max_length=100)
    
    def __str__(self):
        return self.registration_plate

class PersonVehicle(models.Model):
    ''' PersonVehicle register the relatioship between a vehicle in a person,
        in other words the owner of the vehicle at a given point in time '''
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)
    vehicle            = models.ForeignKey(Vehicle, on_delete = models.PROTECT)
    person             = models.ForeignKey(Person, on_delete = models.PROTECT)

    def __str__(self):
        return '{} {}'.format(self.vehicle, self.person)
