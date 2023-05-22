from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import *


# Forms for creating user
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


# Forms of the house
class HouseForm(forms.ModelForm):

    class Meta:
        model = t_house
        fields = ['houCity', 'houPlot', 'houSurface', 'houConstructionYear', 'houFloor', 'houRoom', 'idxHeaterTechnologie']

        city = forms.CharField(max_length=128)
        plot = forms.IntegerField()
        surface = forms.FloatField()
        constructionYear = forms.IntegerField()
        floor = forms.IntegerField()
        room = forms.IntegerField()
        heaterTechnologie = forms.MultipleChoiceField()

        # Name correctly the label with the wanted text label
        labels = {
            'houCity' : 'Ville',
            'houPlot' : 'Parcelle', 
            'houSurface' : 'Surface', 
            'houConstructionYear' : 'Année de construction', 
            'houFloor' : 'Etages',
            'houRoom' : 'Pièces',
            'idxHeaterTechnologie' : 'Technologie de chauffage',
        }


    def __init__(self, *args, **kwargs):
        super(HouseForm, self).__init__(*args, **kwargs)
        self.fields['idxHeaterTechnologie'].queryset = t_heaterTechnologie.objects.all()
        self.fields['houCity'].widget.attrs.update({'class': 'form-control'})
        self.fields['houPlot'].widget.attrs.update({'class': 'form-control'})
        self.fields['houSurface'].widget.attrs.update({'class': 'form-control'})
        self.fields['houConstructionYear'].widget.attrs.update({'class': 'form-control'})
        self.fields['houFloor'].widget.attrs.update({'class': 'form-control'})
        self.fields['houRoom'].widget.attrs.update({'class': 'form-control'})
        self.fields['idxHeaterTechnologie'].widget.attrs.update({'class': 'form-control'})


# 
class PictureForm(forms.ModelForm):

    class Meta:
        model = t_picture
        fields = ['picImage']

        image = forms.ImageField()

        # Name correctly the label with the wanted text label
        labels = {
            'picImage' : 'Images'
        }

        # All the needed widget for the model form fields
        widgets = {
            'picImage' : forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        }

# 
class DocumentForm(forms.ModelForm):

    class Meta:
        model = t_document
        fields = ['docFileUrl']

        file = forms.FileField()

        # Name correctly the label with the wanted text label
        labels = {
            'docFileUrl' : 'Documents annexes'
        }

        # All the needed widget for the model form fields
        widgets = {
            'docFileUrl' : forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
        }