from users.models import Packages, UserProfile
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, ProfileForm

# Create your views here.
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Username or password is incorrect')

    context = {}
    return render(request,'users/login.html',context)

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()
    profileForm = ProfileForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        profileForm = ProfileForm(request.POST)
        if form.is_valid() and profileForm.is_valid():
            userObj = form.save()
            defaultProfile = UserProfile(user = userObj, name = profileForm.cleaned_data.get('name'))
            defaultProfile.save()
            username = form.cleaned_data.get('username')
            messages.success(request,'Account was created for \''+username+'\' successfully')

            return redirect('login')


    context = {'form':form, 'pform': profileForm}
    return render(request,'users/register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

#@login_required(login_url='login')
def homePage(request):
    if request.user.is_authenticated:
        user = request.user
        userProfile = UserProfile.objects.get(user_id = user.id)
        context={"userP": userProfile}
    else:
        context={}
    return render(request,'users/home.html',context)

@login_required(login_url='login')
def profilePage(request):
    user = request.user
    user_packages = Packages.objects.filter(uId = user.id) 
    context={
        'user': user,
        'user_packages': user_packages
    }
    return render(request, 'users/viewprofile.html', context)