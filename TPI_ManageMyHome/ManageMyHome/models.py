from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf.global_settings import *
from django.conf import settings


# Set the documents path and create a folder with the house's id
def documentsPath(instance, filename):
    return "house/documents/{0}/{1}".format(instance.idxHouse.id, filename)

# Set the images path and create a folder with the house's id
def imagesPath(instance, filename):
    return "house/images/{0}/{1}".format(instance.idxHouse.id, filename)


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
    comName = models.CharField(max_length=128)
    comAdress = models.CharField(max_length=128)
    comZip = models.IntegerField(default=0)
    comCity = models.CharField(max_length=128)
    comDomain = models.CharField(max_length=128)
    comPhone = models.IntegerField(default=0)
    comEmail = models.EmailField(max_length=128)
    comImage = models.ImageField(upload_to="company", blank=True, null=True)

    def __str__(self):
        return f"{self.comName}"

# Model for the contact
class t_contact(models.Model):
    conFirstname = models.CharField(max_length=128)
    conLastname = models.CharField(max_length=128)
    conFunction = models.CharField(max_length=128)
    conEmail = models.EmailField(max_length=128)
    conPhone = models.IntegerField(default=0)
    idxCompany = models.ForeignKey(t_company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.conFirstname}"

# Model for the work
class t_work(models.Model):
    worName = models.CharField(max_length=128)
    worCost = models.DecimalField(max_digits=8, decimal_places=2)
    worDescription = models.TextField(blank=False)
    worStart = models.DateField()
    worEnd = models.DateField()
    worContract = models.FileField(upload_to="work/contract", blank=True, null=True)
    worBillUrl = models.FileField(upload_to="work/bill", blank=True, null=True)
    idxCompany = models.ForeignKey(t_company, on_delete=models.CASCADE)
    idxProject = models.ForeignKey(t_project, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.worName}"
