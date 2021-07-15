from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Packages, UserProfile
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name']

class UploadPackageForm(forms.ModelForm):
    class Meta:
        model = Packages
        fields = ['packageName','packageDesc','packageThumbnail','packageItems']