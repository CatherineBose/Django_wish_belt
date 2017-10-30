from __future__ import unicode_literals
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
from datetime import datetime, timedelta, date
from datetime import *
# django.utils.timezone.now()
from django.db import models

class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = []
        if len(self.filter(username=postData['username'])) > 0:
            user = self.filter(username=postData['username'])[0]
            # check this user's password
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append('password incorrect, check if caps lock is on')
        else:
            errors.append('username incorrect')
        if errors:
            return errors
        return user
    def register_validator(self,postData):
        #Initialize empty array for errors 
        errors = [] 
        # check first name and last name length
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors.append("User first name and last name should be more than 2 characters")
        # check password
        if len(postData['password']) < 8:
            errors.append("Password should have more than 8 characters") 
        # check first_name and last_name for valid characters
        if not re.match(nameFilterREGEX, postData['first_name']) or not re.match(nameFilterREGEX, postData['last_name']):
            errors.append("User first name and last name should contains only letters no special characters allowed")  
        # check email with Email_REgex
        if not re.match(emailFilterREGEX, postData['email']):
            errors.append("Not a valid email, check ")
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors.append("email already in use") 
        # check password
        if postData['password'] != postData['confirm']:
            errors.append("Password doesn't match")
        if not errors:
                # add a new user
                # hash password
                hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(5))
                print "hashed code: ", hashed
                new_user = self.create(
                    first_name=postData['first_name'],
                    last_name=postData['last_name'],
                    email=postData['email'],
                    password=hashed
                )
                return new_user
        return errors

class WishManager(models.Manager):
    def itenaryAdd_validator(self,postData):
         #Initialize empty array for errors 
        errors = [] 
        # check destination length
        if len(postData['Item']) < 2: 
            errors.append(" Item should be more than 2 characters")
        # check destination length
        if len(postData['plan']) < 2: 
            errors.append("Travel plan should be more than 2 characters")
        #checking if travel start date is in the past
        if datetime.now() > postData['travel_Start_Date']:
            errors.append("Enter a future date to start your trip")
        #checking if travel end date  is before travel_Start_Date
        if postData['travel_Start_Date']> postData['travel_End_Date']:
            errors.append("Travel end date should be greater than travel start date")
        # check if the particular travel plan exists
        if len(Itenary.objects.filter(destination = postData['destination'])) >0:
            noOfTripsToDestination= len(Itenary.objects.filter(destination = postData['destination']))
            tripsToDestination= Itenary.objects.filter(destination = postData['destination'])
            for i in range (0,noOfTripsToDestination):
                 trip2beVeriyed = tripsToDestination[i]
                 if (trip2beVeriyed.destination == postData['destination'] and trip2beVeriyed.travel_Start_Date == postData['travel_Start_Date'] and trip2beVeriyed.travel_End_Date == postData['travel_End_Date']):
                     errors.append("Trip already planned, plan another trip")
        if not errors:# add a new travel plan
            new_itenary = self.create(
                    item=postData['item'],
                    dateAdded =postData[' dateAdded '])
            #         travel_Start_Date=postData['travel_Start_Date'],
            #         travel_End_Date=postData['travel_End_Date'])
            return new_itenary
        return errors
# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=45)
    # email = models.TextField(max_length=45)
    password = models.CharField(max_length=45)
    objects = UserManager()
    date_hired =models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return "User object:\nid:{} \nname: {}, \nuser_name: {}, \n date_hired:{} ".format(self.id,self.first_name, self.last_name, self.email, self.date_hired)

class Wish(models.Model):
    item = models.CharField(max_length=255)
    dateAdded = models.DateField()
    wisher = models.ForeignKey(User, related_name="wishesForItems")
    addedByWisher = models.ManyToManyField(User, related_name="wishedItem")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()