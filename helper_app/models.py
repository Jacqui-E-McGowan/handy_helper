from django.db import models
from datetime import datetime
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['email'])
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters long'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters long'
        if len(postData['password']) < 8:
            errors['password'] = 'Password cannot be less than 8 characters long'
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = 'Passwords do not match'
        if len(postData['email']) < 1:
            errors['reg_email'] = 'Email address cannot be blank'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['reg_email'] = 'Please enter a valid email address'
        elif check:
            errors['reg_email'] = 'Email address is already registered'
        return errors

    def login_validator(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['login_email'])
        if not check:
            errors['login_email'] = 'Email has not been registered'
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), check[0].password.encode()):
                errors['login_email'] = 'Email and password do not match'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    objects = UserManager()

class JobManager(models.Manager):
    def job_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title'] = "Title must have at least 3 characters"
        if len(postData['description']) < 3:
            errors['description'] = "Description must have at least 3 characters"
        if len(postData['location']) < 3:
            errors['location'] = "Location must have at least 3 characters"
        return errors

    def edit_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title'] = "Title must have at least 3 characters"
        if len(postData['description']) < 3:
            errors['description'] = "Description must have at least 3 characters"
        if len(postData['location']) < 3:
            errors['location'] = "Location must have at least 3 characters"
        return errors

class Job(models.Model):
    CAT_CHOICES = (
        ('Pet Care', 'Pet Care'),
        ('Electrical', 'Electrical'),
        ('Garden', 'Garden'),
    )
    title = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CAT_CHOICES, default=2, null=True)
    created_by = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    add_job = models.ManyToManyField(User, related_name="added")
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    objects = JobManager()