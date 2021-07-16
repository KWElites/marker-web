from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.fields import ImageField
from .models import Package, UserProfile
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class ProfileForm(forms.ModelForm):
   avatar = forms.ImageField(required = False)
   class Meta:
        model = UserProfile
        fields = ['name','avatar']

class UploadPackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['packageName','packageDesc','packageThumbnail','packageItems']
