from django.shortcuts import render, redirect
from . models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


# Create your views here.

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST" :
        username =request.POST['username']
        password =request.POST['password']
        user = authenticate(request, username = username, password= password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else :
            messages.success(request, "There was an error. Please Try Again!")
            return redirect('login')

    else:
        return render(request, 'login.html', {})
   


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out... Thanks for shopping ..."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and return the user instance
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']  # Use 'password1' for the raw password
            
            # Directly log in the user after saving
            login(request, user)
            messages.success(request, ("You have registered successfully!!"))
            return redirect('home')
        
        else:
            # Display error message and render the form again with errors
            messages.error(request, ("Whoops! There was an error, please try again!"))
            return render(request, 'register.html', {'form': form})

    else:
        return render(request, 'register.html', {'form': form})
