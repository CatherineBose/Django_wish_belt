from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import datetime
from time import gmtime, strftime
from . models import *

# urlpatterns = [
#     url(r'^$', views.index),
#     url(r'^register$', views.register),
#     url(r'^login$', views.login),
#     url(r'^success$', views.success),
#     url(r'^logout$', views.logout),
#     url(r'^dashboard$',views.dashboard),
#     url(r'^wish_items/create$',views.createItem),
#     url(r'^wish_items/?P<id>\d+',views.itemAddedByUsers)
   
# ]

def index(request):
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    #Print key value pairs equest.session
    for key,data in request.session.iteritems():
        print key, " = ", data
    return render(request, "yourWish/index.html")

def register(request):
    result = User.objects.register_validator(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    messages.success(request, "Successfully registered!")
    return redirect('/success')

def success(request):
    name = request.session['name'] 
    username = request.session['username']
    userObjArr = User.objects.filter(first_name = fname,last_name = lname) 
    userObj =  userObjArr[0]
    user_id = userObj.id
    try:
        request.session['name'] 
    except KeyError:
        return redirect ('/')
    context ={
        'user': User.objects.get(id=user_id)
    }
    return render(request, "yourWish/success.html", context)
def login(request):
    result = User.objects.login_validator(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect ('/')  
    # #################### Initialize request.session now that user has successfully logged in ########### 
    # request.session['user_id'] = result.id
    request.session['first_name']= result.first_name
    request.session['last_name']= result.last_name
    # del request.session['user_id']
    messages.success(request, "Successfully logged in!")
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    #Print key value pairs equest.session
    for key,data in request.session.iteritems():
        print key, " = ", data
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    # return redirect('/success')
    return redirect('/dashboard')

def logout(request):
    try:
        del request.session['name']
        del request.session['username']
        #Flush the session 
        request.session.flush()
    except KeyError:
        print "Error while trying to logout"
    return HttpResponse("You're logged out.")

def dashboard(request):
    name = request.session['name'] 
    username = request.session['username']
    
    userObjArr = User.objects.filter(name = fname,username = username) 
    print userObjArr[0]
    userObj =  userObjArr[0]
    user_id = userObj.id
    #Lets get the itenaries for the current user 
    wishObjArr = Wish.objects.filter(_id = user_id)
    noOfWishes = len(wishObjArr)
    for wish in wishObjArr:
        print wish.item
        # print wish.travel_Start_Date
        # print wish.travel_End_Date
        # print wish.planth user table obj 
    zipped_list = zip(otherUsersNamesObj, otherUserItenaryArr)
    for a,b in zip(otherUsersNamesObj, otherUserItenaryArr):
        print"in zipped list:"
        # print "name",a.first_name
        # print "destination", b.destination
    # itenaryObj = itenaryObjArr[0]
    # admin = Admin.objects.filter(age__lt=70, first_name__startswith="S")
    #Initialize the context dictionary to be passed to the template in render  
    context ={
        "currentuserFullName" : currentuserFullName, 
        "itenaryObjArr" : itenaryObjArr,
        "otherUserItenaryArr": otherUserItenaryArr,
        "zipped_list" : zipped_list
        # "otherUserItenaryArr": otherUserItenaryArr,
        # "otherUsersNamesObj" : otherUsersNamesObj

    }
       
    return render(request, 'yourWish/dashboard.html',context)
def addItem(request):
    pass
    return redirect('yourWish/create.html')

def home(request):
    pass
    return redirect('/dashboard')

def createItem(request):
    pass
    return render(request, 'yourWish/create.html')

def itemAddedByUsers(request):
    pass
    return render(request, 'yourWish/wishedItems.html')


