
# GreenWich

# Built With

> ### `Django` 
> ### `Django Rest Framework`
> ### `PostgreSQL` 

# Deployed to Netlify (the admin panel connected to an android app)

### [Netlify](https://greenwich.netlify.app/auth)

---
# Getting started
---
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
# Prerequisites
This is a project written using Python, Django and Django Rest Framework
1. Clone the repository
```
https://github.com/luianqi/wushu-book
```
2. Create the virtual enviroment
 ```
python3 -m venv venv
source venv/bin/activate
```
3. Install the requirements
```
pip install -r requirements.txt
```
4. Create a new PostgreSQL database

In your terminal:
```
psql postgres
CREATE DATABASE databasename
\c databasename
```
5. Create a new superuser
```
python manage.py createsuperuser
```
6. Migrate and run migrations
```
python manage.py migrate
python manage.py makemigrations
```
7. Run the project
```
python manage.py runserver
```
