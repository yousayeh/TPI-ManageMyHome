from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf.global_settings import *
from django.conf import settings
from django.core.validators import RegexValidator


# Set the documents path and create a folder with the house's id
def documentsPath(instance, filename):
    return "house/documents/{0}/{1}".format(instance.idxHouse.id, filename)

# Set the images path and create a folder with the house's id
def imagesPath(instance, filename):
    return "house/images/{0}/{1}".format(instance.idxHouse.id, filename)

# Set the contract path and create a folder with the username
def contractPath(instance, filename):
    return "work/contract/{0}/{1}".format(instance.idxProject.idxUser.username, filename)

# Set the bill path and create a folder with the username
def billPath(instance, filename):
    return "work/bill/{0}/{1}".format(instance.idxProject.idxUser.username, filename)

# Set the logo path and create a folder with the company name
def logoPath(instance, filename):
    return "company/{0}/{1}".format(instance.comName, filename)

# Regex for company name and phone numbers
alphanumericValidator = RegexValidator(r'^[A-Za-z0-9 -]*[A-Za-z0-9][A-Za-z0-9 -]*$', 'Seule les caractères alphanumeric et les tirets sont autorisées')
phoneNumberValidator = RegexValidator(r'(\+41|0041|0){1}(\(0\))?[0-9]{2}[\s.-]?[0-9]{3}[\s.-]?[0-9]{2}[\s.-]?[0-9]{2}$', 'Veuillez entrez un numéro de téléphone suisse valide.')



# Model for the users
class t_user(AbstractUser):
    pass

# Model for the heaters technologie
class t_heaterTechnologie(models.Model):
    heaName = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.heaName}"

# Model for the house
class t_house(models.Model):
    idxUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    houCity = models.CharField(max_length=128)
    houPlot = models.IntegerField(default=0)
    houSurface = models.FloatField(default=0.0)
    houConstructionYear = models.IntegerField(default=0)
    houFloor = models.IntegerField(default=0)
    houRoom = models.IntegerField(default=0)
    idxHeaterTechnologie = models.ForeignKey(t_heaterTechnologie, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.id}"

# Model for the documents
class t_document(models.Model):
    docFileUrl = models.FileField(upload_to=documentsPath, blank=True, null=True)
    idxHouse = models.ForeignKey(t_house, on_delete=models.CASCADE)

# Model for the image gallery
class t_picture(models.Model):
    picImage = models.ImageField(upload_to=imagesPath, blank=True, null=True)
    idxHouse = models.ForeignKey(t_house, on_delete=models.CASCADE)

# Model for the project
class t_project(models.Model):
    proName = models.CharField(max_length=128)
    idxUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.proName}"

# Model for the link between t_house and t_project
class t_provide(models.Model):
    idxHouse = models.ForeignKey(t_house, on_delete=models.CASCADE)
    idxProject = models.ForeignKey(t_project, on_delete=models.CASCADE)

# Model for the company
class t_company(models.Model):
    comName = models.CharField(max_length=128, validators=[alphanumericValidator])
    comAdress = models.CharField(max_length=128)
    comZip = models.IntegerField(default=0)
    comCity = models.CharField(max_length=128)
    comDomain = models.CharField(max_length=128)
    comPhone = models.CharField(max_length=16, validators=[phoneNumberValidator])
    comEmail = models.EmailField(max_length=128)
    comImage = models.ImageField(upload_to=logoPath, blank=False, null=False)

    def __str__(self):
        return f"{self.comName}"

# Model for the contact
class t_contact(models.Model):
    conFirstname = models.CharField(max_length=128)
    conLastname = models.CharField(max_length=128)
    conFunction = models.CharField(max_length=128)
    conEmail = models.EmailField(max_length=128)
    conPhone = models.CharField(max_length=16, validators=[phoneNumberValidator])
    idxCompany = models.ForeignKey(t_company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.conFirstname} {self.conLastname}"

# Model for the work
class t_work(models.Model):
    idxProject = models.ForeignKey(t_project, on_delete=models.CASCADE)
    worName = models.CharField(max_length=128)
    worCost = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    worDescription = models.TextField(blank=False)
    worStart = models.DateField()
    worEnd = models.DateField()
    worContract = models.FileField(upload_to=contractPath, blank=False, null=False)
    worBillUrl = models.FileField(upload_to=billPath, blank=False, null=False)
    idxCompany = models.ForeignKey(t_company, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.worName}"
