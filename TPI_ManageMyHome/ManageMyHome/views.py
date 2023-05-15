from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from ManageMyHome.models import *
from django.http import HttpResponse

# Send the index and get all the works from database.
def index(request):
    return render(request, 'index.html', context={"works": "test"})

# Login fonction for users
def loginUser(request):
    page = 'login'
    # True if we're using POST and that the form is valid
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        # Authenticate the user after if he exist
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Identifiant ou mot de passe incorrect.")

    return render(request, 'loginRegister.html', {'page': page})

# Lougout fonction for users
def logoutUser(request):
    logout(request)

    return redirect('login')

# Add user in the database with the ModelForms
def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm

    # True if we're using POST and that the form is valid
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.save()

            user = authenticate(request, username=user.username, password=request.POST['password1'])

            # Authenticate the user after he's been created
            if user is not None:
                login(request, user)
                return redirect('index')

    return render(request, 'loginRegister.html', context = {'form': form, 'page': page})