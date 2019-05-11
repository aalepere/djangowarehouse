# Django datawarehouse
This repo contains the code to support the article published on Medium.
https://medium.com/@arnaud_76506/implementing-a-data-warehouse-with-django-e4856c92f146

## 1 Libraries
A requirements file has been created so you can set up your own virtual env and then install libraries as listed in requirements.txt

### Virtual env
Please make sure you have installed virtual env library first: https://docs.python.org/3/library/venv.html
```shell
virtualenv env
source env/bin/activate
```

### Install requirements
```shell
pip install -r requirements.txt
```

## 2 Django
When you clone the repository you would not require to do this; but to set up a new project and app please refer to the Django documentation or tutorial: https://docs.djangoproject.com/en/2.1/intro/tutorial01/

Remember to run makemigrations and migrate to initiate the database
```shell
.\manage.py makemigrations
.\manage.py migrate
```

## 3 Implementing a Data Warehouse with Django
In this article, we will cover how to leverage Django and its rest framework to implement a data warehouse. We will particularly focus on data sources that come from external APIs but the same principle could be applied to any other types of data sources: flat files or direct ODBC connections.

One of the main benefits of using Django for implementing a data warehouse is that you will be able to use Python for any components or task: ETL, querying, data manipulation, reporting, web app applications …

Please note that Django might not be the right solution for your use case however the same principles can be applied.

All the code used in this article can be found on GitHub.

### What is a data warehouse?
Data warehouses are usually implemented to consolidate different data sources across a company. In our case, we are using different external and internal APIs and we want to consolidate all this information for analysis, reporting and predictive modelling.

The main challenges being to extract, transform and load the data from the different sources into a common format and being able to track changes to the data over time.

We will cover those challenges in the details in the below sections.

### Django and the rest framework
Django is open-source web framework template; and follows the Model, View, Template (MVT) design patterns. In this article, we will mainly focus on the Model component of the Django architecture.
To be able to interact with the database, Django uses an Object Relational Mapper; meaning that instead of using SQL tables they will be represented as Python classes. Which means that we can perform any CRUD operations using Python without the need to interact directly with the SQL or the database itself. 
This will be key in the implementation of our data warehouse as we will leverage this ORM to perform the inserts, updates, …

The Rest-Framework is part of the Django ecosystem and is a useful toolkit to create web APIs.
The component of that framework that we will be using is called serializers; which allow to serialize complex data structures to a render JSON (a typical GET request) but also to parse data to be converted back into complex types, after first validating the incoming data (also called deserialization). 
Which in our case will be extremely useful as we can leverage deserialization to ensure the information is coming in the right format and we can map each element to the right field in our data warehouse.
- https://www.djangoproject.com/
- https://www.django-rest-framework.org/

We will explain how to implement our data warehouse by adding each feature once at the time.

### Basic model
Once we have created both our Django project and app (https://docs.djangoproject.com/en/2.1/intro/tutorial01/); we can now create our model.

Models.py will contain all the logic that allows the Django ORM to interact with the database; each of the class in models.py is a physical table in the database.

In this example we are going to create 3 tables:
- Person; an instance of a physical person uniquely identified by its first name and last name
- Vehicle; vehicle uniquely identified by its registration number
- PersonVehicle; an instance of vehicle ownership by a person

`ADD DIAGRAM`

```python
from django.db import models

class Person(models.Model):
    """ Person class identifies a unique physical person by its first name, last name and email """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Vehicle(models.Model):
    """ Vehicle class uniquely with the registration plate number """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    registration_plate = models.CharField(max_length=100)

    def __str__(self):
        return self.registration_plate


class PersonVehicle(models.Model):
    """ PersonVehicle register the relationship between a vehicle in a person,
        in other words, the owner of the vehicle at a given point in time """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)

    def __str__(self):
        return "{} {}".format(self.vehicle, self.person)
```

`created_at`, `updated_at` are 2 automatically generated fields that will record the date time when the record was created or updated. 

PROTECT will prohibit any deletion of records with relationships with other tables. You can also use CASCADE if you wish to delete all the records related to that record.

Now that we have created our model, we can insert information:
```python
>>>from dwh_app.models import Person
>>>p = Person(first_name="Arnaud", last_name="Alepee", email="alpha@beta.com") 
>>>p.save()
>>>p
<Person: Arnaud Alepee>
```

### Tracking changes
In order to be able to track changes over time, we will be using simple history; which allows storing Django model state on every create/update/delete: https://django-simple-history.readthedocs.io/en/2.7.0/

```python
from django.db import models
from simple_history.models import HistoricalRecords


class Person(models.Model):
    """ Person class identifies a unique physical person by its first name, last name and email """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    history = HistoricalRecords()

    class Meta:
        unique_together = (("first_name", "last_name"),)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Vehicle(models.Model):
    """ Vehicle class uniquely with the registration plate number """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    registration_plate = models.CharField(max_length=100)

    def __str__(self):
        return self.registration_plate


class PersonVehicle(models.Model):
    """ PersonVehicle register the relationship between a vehicle in a person,
        in other words, the owner of the vehicle at a given point in time """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    history = HistoricalRecords()

    class Meta:
        unique_together = (("vehicle"),)

    def __str__(self):
        return "{} {}".format(self.vehicle, self.person)
```

None that we had the field `history` in each model where we wished to track changes over time. These changes will be stored in a mirror table with prefix `history`.

In order to be able to track changes we also need to define `surrogate keys`, these keys are the business definition of uniqueness. For example, in the `Person` table, we defined `first_name` and `last_name` as `unique_together`, which means that those fields will not be updatable however `email` is.

Now let's try to modify the record we recorded before:
```python
>>>from dwh_app_simple_history.models import Person
>>>p = Person.objects.get(first_name="Arnaud", last_name="Alepee")
>>>p.email
'alpha@beta.com'
>>>p.email="new@email.com"
>>>p.save()
'new@email.com'
```

Now let's have a look in the historical table to see how changes have been recorded:
```python
>>>from dwh_app_simple_history.models import Person
>>> Person.history.all()
<QuerySet [{'id': 1, 'created_at': datetime.datetime(2019, 5, 5, 21, 18, 52, 55293, tzinfo=<UTC>), 'updated_at': datetime.datetime(2019, 5, 6, 17, 36, 48, 349931, tzinfo=<UTC>), 'first_name': 'Arnaud', 'last_name': 'Alepee', 'email': 'new@email.com', 'history_id': 2, 'history_date': datetime.datetime(2019, 5, 6, 17, 36, 48, 352849, tzinfo=<UTC>), 'history_change_reason': None, 'history_type': '~', 'history_user_id': None}, 
{'id': 1, 'created_at': datetime.datetime(2019, 5, 5, 21, 18, 52, 55293, tzinfo=<UTC>), 'updated_at': datetime.datetime(2019, 5, 5, 21, 18, 52, 55340, tzinfo=<UTC>), 'first_name': 'Arnaud', 'last_name': 'Alepee', 'email': 'alpha@beta.com', 'history_id': 1, 'history_date': datetime.datetime(2019, 5, 5, 21, 18, 52, 55837, tzinfo=<UTC>), 'history_change_reason': None, 'history_type': '+', 'history_user_id': None}]>
```

### Serializers
As explained previously, serializers will be used to parse and validate the input date before inserting the same in the relevant SQL tables.

Now let's assume that external sources provide us information as per the below JSON format:
```json
{
    "first_name" : "Arnaud",
    "last_name": "Alepee",
    "email": "alpha@beta.com",
    "vehicles": [
        {"registration_plate": "XYZ 123"},
        {"registration_plate": "ABC 456"}]
}
```

The JSON provides the identity of person and list of vehicles that currently belongs to this person, below are the serializers that will be used to parse this JSON:
```python
from rest_framework import serializers

from dwh_app_simple_history.models import Person, PersonVehicle, Vehicle


class VehicleSerializer(serializers.Serializer):
    """
    Nested serializer within the JSON source; in this example all vehicles that belong to the
    person nested in the JON as a list of all active vehicles.
    """

    registration_plate = serializers.CharField(max_length=100)


class PersonVehicleSerializer(serializers.Serializer):
    """
    Serializer that will be used to deserialize the json to be then imported in the datawarehouse
    """

    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)
    vehicles = VehicleSerializer(many=True)

    def save(self):
        """
        Overwrite the save function on the serializer to be able to control how we want to
        insert/update the data provided by the source in our datawarehouse.
        """

        # First update or create the person
        person_obj, created = Person.objects.update_or_create(
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            defaults={"email": self.validated_data["email"]},
        )

        # Then create each Vehicle and link it to the person created before
        for vehicle in self.validated_data["vehicles"]:
            vehicle_obj, created = Vehicle.objects.get_or_create(registration_plate=vehicle["registration_plate"])
            personvehicle_obj, created = PersonVehicle.objects.update_or_create(
                vehicle=vehicle_obj, defaults={"person": person_obj}
            )
```

First, we have created a nested serializer `VehicleSerializer` that parse an instance of one vehicle, then in the parent serializer `PersonVehicleSerializer` we can use the argument `many=True` to tell django that they could be multiple vehicles.

In order to save all information correctly we overwrite the `save()` method, first we create or update the `Person`, then for each vehicle in the nested dictionary we create a `Vehicle` and then link it to the `Person` in `PersonVehicle`.

```python
>>>from dwh_app_simple_history.serializers import PersonVehicleSerializer
>>>from dwh_app_simple_history.models import PersonVehicle 
>>>import json
>>>with open("dwh_app_simple_history/data/sample.json","r") as file: 
      data = json.load(file) 
>>>ser = PersonVehicleSerializer(data=data) 
>>>ser.is_valid()
True
>>>ser.validated_data
OrderedDict([('first_name', 'Arnaud'),
             ('last_name', 'Alepee'),
             ('email', 'alpha@beta.com'),
             ('vehicles',
              [OrderedDict([('registration_plate', 'XYZ 123')]),
               OrderedDict([('registration_plate', 'ABC 456')])])])
>>>ser.save()
<QuerySet [<PersonVehicle: XYZ 123 Arnaud Alepee>, <PersonVehicle: ABC 456 Arnaud Alepee>]>
```

Please note that serializers can be enriched by addind validation or transformation rules if need be like you would do in a traditional ETL implementation.

### Views
In the previous example, we were using a json file and django shell to insert data into our datawarehouse. Let's take this forward by adding a `view` that will allow inserting data through a `POST` api request.

```python
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dwh_app_simple_history.serializers import PersonVehicleSerializer


@api_view(["POST"])
def PersonVehicle(request):
    """
    This view will be called through a POST request to add or update the information provided in
    the request
    """

    # Deserialize the information provided in the request
    ser = PersonVehicleSerializer(data=request.data)

    # Validate the information provided
    ser.is_valid(raise_exception=True)

    # Save the information in the datawarehouse
    ser.save()

    return Response({"All good, everything has been saved"})
```

As you can see we use the same sequence that we used in django shell, but using the `api_view` decorator to expose this endpoint to another system or user. Which means that we can now communicate with our datawarehouse from any system (you need to make sure you django server is running).

```shell
>>>curl -H "Content-Type: application/json" -d @sample.json -X POST http://127.0.0.1:8000/PersonVehicle/add/
["All good, everything has been saved"]
```

## Conclusion
In this article, we have covered all the steps and components of building a datwarehouse with django:
- Use the django ORM to create 3rd normal form data model;
- Use simple history to track changes over time;
- Use serializer the rest framework for deserializing source files and save the results in the datawarehouse; and
- Use views from the rest framework to allow source systems to send information through a POST request.

All the above, should give enough information to build your own datawarehouse, of course, you will have to go through all the different sources, understand how the data will be used downstream to model the data in the most efficient way, and add all transformation/validation rules in your ETL.
