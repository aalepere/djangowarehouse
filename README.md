# djangowarehouse
This repo contains the code to support the article published on Medium

## 1 Libraries
A requirements file has been created so you can setup your own virtual env and then install libraries as listed in requirements.txt

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
When you clone the repository you would not require to do this; but to setup a new project and app please refer to the Django documentation or tutorial: https://docs.djangoproject.com/en/2.1/intro/tutorial01/

Remember to run makemigrations and migrate to initiate the database
```shell
.\manage.py makemigrations
.\manage.py migrate
```

## 3 Implementing a Data Warehouse with Django
In this article, we will cover how to leverage Django and its rest framework to implement a data warehouse. We will particularly focus on data sources that come from external APIs but the same principle would apply to any other types of data sources: flat files or direct ODBC connections.
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
The Rest-Framework is part of the Django ecosystem and is a useful toolkit to create web APIs. We don't really need to create web APIs for our data warehouse however we can re-use some of the components for any new information which is similar to a POST request in a way.
The component of that framework that we will be using is called serializers; which allow to serialize complex data structures to a render JSON (a typical GET request) but also to parse data to be converted back into complex types, after first validating the incoming data (also called deserialization). Which in our case will be extremely useful as we can leverage deserialization to ensure the information is coming in the right format and we can map each element to the right field in our data warehouse.
https://www.djangoproject.com/
We will explain how to implement our data warehouse by adding each feature once at the time.

### Basic model
Once we have created both our Django project and app (https://docs.djangoproject.com/en/2.1/intro/tutorial01/); we can now create our model.
Models.py will contain all the logic that allows the Django ORM to interact with the database; each of the class in models.py is a physical table in the database.
In this example we are going to create 3 tables:
Person; an instance of a physical person uniquely identified by its first name and last name
Vehicle; vehicle uniquely identified by its registration number
PersonVehicle; an instance of vehicle ownership by a person

`ADD DIAGRAM`

`created_at`, `updated_at` are 2 automatically generated fields that will record the date time when the record was created or updated. PROTECT will prohibit any deletion of records with relationships with other tables. You can also use CASCADE if you wish to delete all the records related to that record.
Now that we have created our model, we can insert information:

```python
ADD CODE
```

### Tracking changes
In order to be able to track changes over time, we will be using simple history; which allows storing Django model state on every create/update/delete: https://django-simple-history.readthedocs.io/en/2.7.0/
Now let's try to modify an existing record:

```pyhton
ADD CODE
```
