from django.db import models
import re
from datetime import datetime
from .models import *



#VALIDATION CLASS/basic_validator
class UserManager(models.Manager):
    def basic_validator(self, postData):

        errors = {}

        if len(postData['first_name']) < 2:
           errors['first_name'] = "First name should be longer than 2 characters"


        if len(postData['last_name']) < 2:
           errors['last_name'] = "Last name should be longer than 2 characters"
        
        #checking the fomrmat of the entered email!!
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")

        #matching the passwords
        if postData['password'] != postData['password_confirm']:
            errors['passwordMatch'] = "Passwords do not match!"
        
        if len(postData['password']) < 8:
            errors['passwordLength'] = "Password should be longer than 8 characters"

        return errors


    
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid email address!")

        # if postData['password'] != postData['password']:
        #             errors['passwordMatch'] = "Passwords do not match!"
                
        if len(postData['password']) < 8:
            errors['password'] = "Password should be longer than 8 characters"



        return errors



#BOOK VALIDATOR INFO
class BookManager(models.Manager):
    def basic_validator(self, postData):

        errors = {}

        if len(postData['title']) < 1:
           errors['title'] = "Title is required"


        if len(postData['desc']) < 5:
           errors['desc'] = "Description should be longer than 5 characters"

        return errors


# classes!!

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=150)

    #ONE TO MANY
    #liked_books list of obooks liked by user

    #books_uploaded list of books uplaoded by user

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #PASS VALIDATION MANAGER
    objects = UserManager()


class Book(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField(max_length=100)

    #ONE to MANY  uploaded by and liked books
    uploaded_by = models.ForeignKey(User, related_name='books_uploaded')
    #user who uplaoded the book

    #MANY to MANY Relationship!!!
    users_who_liked = models.ManyToManyField(User, related_name="liked_books")
    #list of users who like a given book


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #PASSING BOOK VALIDATION
    objects = BookManager()
