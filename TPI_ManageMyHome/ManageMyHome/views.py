from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from ManageMyHome.models import *
from django.http import HttpResponse
from django.db.models import Q
import os

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

# Add the works
@login_required(login_url = 'login')
def addWorkProject(request):
    # Get the current user
    currentUser = request.user
    # Create all the needed forms using forms.py
    formWork = WorkForm(user=currentUser)
    formProject = ProjectForm()

    # True if we're using POST method
    if request.method == 'POST':
        # Check for wich form has been submitted
        if 'btnSubmitWork' in request.POST:
            # Generate work form
            formWork = WorkForm(request.POST, request.FILES, user=currentUser)

            # Check for the forms validation
            if formWork.is_valid():

                # Save the work data in the database
                work = formWork.save(commit=False)
                work.idxUser = currentUser
                work.save()

                return redirect('index')

        if 'btnSubmitProject' in request.POST:
            # Generate the project form
            formProject = ProjectForm(request.POST)

            # Check for the forms validation
            if formProject.is_valid():
                
                # Save the project data in the database
                project = formProject.save(commit=False)
                project.idxUser = currentUser
                project.save()

                # Add the link between the projects and the house
                lastHouse = t_house.objects.filter(idxUser=request.user.id).latest('id')
                lastPoject = t_project.objects.filter(idxUser=request.user.id).last()

                t_provide.objects.create(idxHouse=lastHouse, idxProject=lastPoject)

                return redirect('addWorkProject')

    return render(request, 'addWorkProject.html', context={'formWork': formWork, 'formProject': formProject})

# Update the works
@login_required(login_url = 'login')
def updateWork(request, workId):
    # Get the current user
    currentUser = request.user
    # Get the work with the id
    work = t_work.objects.get(pk=workId)

    # Create form using forms.py
    formWork = WorkForm(instance=work, user=currentUser)
    
    # True if we're using POST method
    if request.method == 'POST':
        # Generate the form
        formWork = WorkForm(request.POST, request.FILES, instance=work, user=currentUser)

        # Get the contract and bill path
        pathContract = work.worContract.path
        pathBill = work.worBillUrl.path

        # Get all the files uploaded
        contract = request.FILES.getlist('worContract')
        bill = request.FILES.getlist('worBillUrl')

        # Check for the form validation
        if formWork.is_valid():

            # Check if the user uploaded new files
            if len(request.FILES) != 0:
                # Delete the old file
                if len(contract) > 0:
                    os.remove(pathContract)

                if len(bill) > 0:
                    os.remove(pathBill)

            # Save the data in database
            formWork.save()

            return redirect('index')


    return render(request, 'updateWork.html', context={'formWork': formWork})

# Delete a work with the link
@login_required(login_url = 'login')
def deleteWork(request, workId):
    # Get the work wanted to be deleted
    work = get_object_or_404(t_work, pk=workId)

    # Delete the contract stored in the work's directory
    os.remove(work.worContract.path)

    # Delete the bill stored in the work's directory
    os.remove(work.worBillUrl.path)

    # Delete the work
    work.delete()

    return redirect('index')

# Show all the infos of one work
@login_required(login_url = 'login')
def detailWork(request, workId):
    # Get the selected work
    work = get_object_or_404(t_work, pk=workId)


    return render(request, 'detailWork.html', context={"work": work})

# Update the project
@login_required(login_url = 'login')
def updateProject(request, projectId):
    # Get the project with the id
    project = t_project.objects.get(pk=projectId)

    # Create form using forms.py
    form = ProjectForm(instance=project)

    # True if we're using POST method
    if request.method == 'POST':
        # Generate the form
        form = ProjectForm(request.POST, instance=project)

        # Check for the form validation
        if form.is_valid():

            # Save the project data in the database
            form.save()

            return redirect('index')

    return render(request, 'updateProject.html', context={'form': form})

# Delete a project with the link
@login_required(login_url = 'login')
def deleteProject(request, projectId):
    # Get the project wanted to be deleted
    project = get_object_or_404(t_project, pk=projectId)

    # Delete the project 
    project.delete()

    return redirect('index')

# Show all the infos of the house
@login_required(login_url = 'login')
def myHouse(request, userId):
    # Get the user's house 
    house = t_house.objects.filter(idxUser=userId)
    # Get the user's house pictures
    pictures = t_picture.objects.filter(idxHouse__in=house)
    # Get the user's house documents
    documents = t_document.objects.filter(idxHouse__in=house)

    # Verify if the house exist, create the request and get the info if yes or redirect to the forms if not
    if house.exists():
        house = get_object_or_404(t_house, idxUser=userId)
    else:
        return redirect('addHouse')


    return render(request, 'myHome.html', context={"house": house, "pictures": pictures, "documents": documents})

# Add the user's house with the house's images gallery and related documents
@login_required(login_url = 'login')
def addHouse(request):
    # Get the current user
    currentUser = request.user
    # Create all the needed forms using forms.py
    formHouse = HouseForm()
    formPicture = PictureForm()
    formDocument = DocumentForm()

    # True if we're using POST method
    if request.method == 'POST':
        # Generate the main house form
        formHouse = HouseForm(request.POST)
        # Get all the files uploaded
        images = request.FILES.getlist('picImage')
        files = request.FILES.getlist('docFileUrl')

        # Check for the forms validation
        if formHouse.is_valid():

            # Save the basic house data in the database
            house = formHouse.save(commit=False)
            house.idxUser = currentUser
            house.save()

            # Get the house's id
            lastHouse = t_house.objects.filter(idxUser=request.user.id).latest('id')

            # Add all the image's path in the database linked by the house's id
            for image in images:
                t_picture.objects.create(picImage=image, idxHouse=lastHouse)

            # Add all the documents's path in the database linked by the house's id
            for file in files:
                t_document.objects.create(docFileUrl=file, idxHouse=lastHouse)

            return redirect('myHouse', userId=request.user.id)

    return render(request, 'addHouse.html', context={'formHouse': formHouse, 'formPicture': formPicture, 'formDocument': formDocument})

# Update the user's house with the house's images gallery and related documents
@login_required(login_url = 'login')
def updateHouse(request, houseId):
    # Get the house with the id
    house = t_house.objects.get(pk=houseId)
    # Get all the pictures for the house
    images = t_picture.objects.filter(idxHouse=houseId)
    # Get all the documents for the house
    documents = t_document.objects.filter(idxHouse=houseId)

    # Generate the Forms
    formHouse = HouseForm(instance=house)
    formPicture = PictureForm()
    formDocument = DocumentForm()

    # True if we're using POST method
    if request.method == 'POST':
        # Generate the main house form
        formHouse = HouseForm(request.POST, instance=house)
        # Get all the files uploaded
        imagesFiles = request.FILES.getlist('picImage')
        files = request.FILES.getlist('docFileUrl')

        # Check for the forms validation
        if formHouse.is_valid():

            # Check if the user uploaded new files
            if len(request.FILES) != 0: 
                if len(imagesFiles) > 0:
                    # Delete the images stored and the URL record in the database 
                    for image in images:
                        os.remove(image.picImage.path)
                        image.delete()
                # Add the new images
                for imageFile in imagesFiles:
                    t_picture.objects.create(picImage=imageFile, idxHouse=house)

                if len(files) > 0:
                    # Delete the documents stored and the URL record in the database 
                    for document in documents:
                        os.remove(document.docFileUrl.path)
                        document.delete()
                # Add the new documents
                for file in files:
                    t_document.objects.create(docFileUrl=file, idxHouse=house)

            # Save the data in database
            formHouse.save()

            return redirect('myHouse', userId=request.user.id)


    return render(request, 'updateHouse.html', context={'formHouse': formHouse, 'formPicture': formPicture, 'formDocument': formDocument})

# Delete a house with the link
@login_required(login_url = 'login')
def deleteHouse(request, houseId):
    # Get the house wanted to be deleted
    house = get_object_or_404(t_house, pk=houseId)
    # Get all the pictures for the house
    images = t_picture.objects.filter(idxHouse=houseId)
    # Get all the documents for the house
    documents = t_document.objects.filter(idxHouse=houseId)
    # ToDo : Delete the projects too ?

    # Delete all the images stored in the house's directory
    for image in images:
        os.remove(image.picImage.path)

    # Delete all the documents stored in the house's directory
    for document in documents:
        os.remove(document.docFileUrl.path)

    # Delete the house
    house.delete()

    return redirect('index')

# List all the companies
@login_required(login_url = 'login')
def listCompanies(request):
    # Get all the companies
    companies = t_company.objects.all()
    # Get all the contacts
    contacts = t_contact.objects.all()

    return render(request, 'listCompanies.html', context={'companies': companies, 'contacts': contacts})

# Add a company or a contact
@login_required(login_url = 'login')
def addCompanyContact(request):
    # Create all the needed forms using forms.py
    formComany = CompanyForm()
    formContact = ContactForm()

    # True if we're using POST method
    if request.method == 'POST':

        # Check for wich form has been submitted
        if 'btnSubmitCompany' in request.POST:

            # Generate company form
            formComany = CompanyForm(request.POST, request.FILES)

            # Check for the forms validation
            if formComany.is_valid():

                # Save the company data in the database
                formComany.save()

                return redirect('listCompanies')

        if 'btnSubmitConact' in request.POST:

            # Generate the contact form
            formContact = ContactForm(request.POST)

            # Check for the forms validation
            if formContact.is_valid():
                
                # Save the contact data in the database
                formContact.save()

                return redirect('listCompanies')

    return render(request, 'addCompanyContact.html', context={'formComany': formComany, 'formContact': formContact})

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