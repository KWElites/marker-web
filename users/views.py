from users.models import Package, UserProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, ProfileForm, UploadPackageForm
import os

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

def homePage(request):
    if request.user.is_authenticated:
        user = request.user
        userProfile = UserProfile.objects.get(user_id = user.id)
        context={"userP": userProfile}
    else:
        context={}
    return render(request,'users/home.html',context)

def profilePage(request, username):
    user = User.objects.get(username = username)
    userProfile = UserProfile.objects.get(user_id = user.id)
    user_packages = Package.objects.filter(uId = user.id) 
    context={
        'user': user,
        'userP': userProfile,
        'user_packages': user_packages
    }
    return render(request, 'users/viewprofile.html', context)

@login_required(login_url='login')
def editProfile(request):
    user = request.user
    passChangeForm = PasswordChangeForm(user = user)
    userProfile = UserProfile.objects.get(user_id = user.id)
    currentPP = userProfile.avatar
    userProfile.avatar = None

    form = CreateUserForm(instance = user)
    profileForm = ProfileForm(instance = userProfile)

    if request.method == 'POST':
        if "save_details" in request.POST:
            profileForm = ProfileForm(request.POST,request.FILES)

            if profileForm.is_valid():
                newUserProfile = profileForm.save(commit=False)
                userProfile.name = newUserProfile.name
                if request.POST.get('clearPP') == "on":
                    userProfile.avatar = "profilePics/defaultPP.jpg"
                elif os.path.basename(os.path.normpath(newUserProfile.avatar.url)) != "defaultPP.jpg":
                    userProfile.avatar = newUserProfile.avatar
                else :
                    userProfile.avatar = currentPP
                
                userProfile.save() 
                return redirect("profile", user.username)
        
        if "change_pass" in request.POST:
            passChangeForm = PasswordChangeForm(user = request.user, data = request.POST)
            if passChangeForm.is_valid():
                user = passChangeForm.save()
                update_session_auth_hash(request, user)
                return redirect("profile", user.username)

    context = {
        'user':user,
        'form':form, 
        'pform': profileForm,
        'passChangeForm': passChangeForm
    }
    return render(request, 'users/editprofile.html', context)

@login_required(login_url='login')
def uploadPage(request):
    uploadForm = UploadPackageForm()
    if request.method == 'POST':
        uploadForm = UploadPackageForm(request.POST,request.FILES)
        if uploadForm.is_valid():
            uploadedPackage = uploadForm.save(commit=False)
            uploadedPackage.packageItems = request.FILES['packageItems']
            uploadedPackage.uId = request.user
            #fileType stores the extension of the package, for later checking that it's a .zip file
            fileType = uploadedPackage.packageItems.url.split('.')[-1]
            fileType = fileType.lower()
            if fileType != 'zip':
                return redirect('upload')
            uploadedPackage.save()
            print('package '+uploadedPackage.packageName+' saved')
            return redirect('home')
    context={'packageForm':uploadForm}
    return render(request,'users/upload.html',context)