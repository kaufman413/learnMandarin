from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from main.models import UserProfile

# Create your views here.
def index(request):
    #return HttpResponse("我要学习中文!")
    return render(request, 'homepage/homepage.html', {})

def registration(request):
    return render(request, 'homepage/registration.html', {})

def registerUser(request):
    username = request.POST['username']
    password = request.POST['password']
    #retyped_password = request.POST['rpassword']
    email    = request.POST['email']

    #check to see that username doesn't already exist
    if User.objects.filter(username=username).exists():
        error = "username already exists"
        return render(request, 'homepage/registration.html', {"error":error})

    # check that passwords match and are >= 5 characters
    if len(password) < 7:
        error = "password must be at least 7 characters long"
        return render(request, 'homepage/registration.html', {"error": error})

    else: #create a user and log them in
        #User Profile Object
        newUser = UserProfile(username=username, points=0)
        newUser.save()
        #django user
        User.objects.create_user(username, email, password)
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('main/')


def loginUser(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('main/')
    else:
        content = "FAIL!"
        return render(request, 'homepage/loginUser.html', {"content":content})

