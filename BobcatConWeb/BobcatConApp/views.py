from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .forms import CreateUserForm


def home(request):
    return render(request, 'registration/homepage.html')

def login(request):
    return render(request, 'registration/login.html')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        
    context = {'registerform' : form}
    return render(request, 'registration/signup.html', context=context)
 

def logout(request):
    pass