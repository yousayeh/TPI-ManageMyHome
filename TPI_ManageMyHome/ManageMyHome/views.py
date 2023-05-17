from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from ManageMyHome.models import *
from django.http import HttpResponse
from django.db.models import Q

# Send the index and get all the works from database.
def index(request):
    # Get the current user's id
    user = request.user.id

    if user is not None:
        # Get the current user
        user = request.user
        # Get all the projects created by user
        projects = t_project.objects.filter(idxUser=user)
        # Get all the works for each projects created by user
        works = t_work.objects.filter(idxProject__in=projects)

        # Get all the companies
        companies = t_company.objects.all()

        # Allows the user to research a work or a company
        if request.method == "POST":
            searched = request.POST['search']
            works = t_work.objects.filter(worName__contains=searched).filter(idxProject__in=projects)
            companies = t_company.objects.filter(comName__contains=searched)
    else :
        # Get all the works
        works = t_work.objects.all()
        # Get all the companies
        companies = t_company.objects.all()

        # Allows the user to research a work or a company
        if request.method == "POST":
            searched = request.POST['search']
            works = t_work.objects.filter(worName__contains=searched)
            companies = t_company.objects.filter(comName__contains=searched)

    return render(request, 'index.html', context={"works": works, "companies": companies})

# Delete a work with the link
@login_required(login_url = 'login')
def deleteWork(request, workId):
    work = get_object_or_404(t_work, pk=workId)
    work.delete()

    return redirect('index')

# Show all the infos of one work
@login_required(login_url = 'login')
def detailWork(request, workId):
    # Get the selected work
    work = get_object_or_404(t_work, pk=workId)


    return render(request, 'detailWork.html', context={"work": work})

# Show all the infos of the house
@login_required(login_url = 'login')
def myHouse(request, userId):
    # Get the user's house
    house = t_house.objects.filter(idxUser=userId)

    # Verify if the house exist, create the request and get the info if yes or redirect to the forms if not
    if house.exists():
        house = get_object_or_404(t_house, idxUser=userId)
    else:
        # ToDo : redirect to the forms
        return redirect('index')


    return render(request, 'myHome.html', context={"house": house})

# Delete a house with the link
@login_required(login_url = 'login')
def deleteHouse(request, houseId):
    house = get_object_or_404(t_house, pk=houseId)
    house.delete()

    return redirect('index')

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