from users.models import Package, UserProfile
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, ProfileForm, UploadPackageForm
import zipfile
from os import path

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
    user_packages = Package.objects.filter(uId = user.id) 
    context={
        'user': user,
        'user_packages': user_packages
    }
    return render(request, 'users/viewprofile.html', context)

def validZip(uploadedZip):
    validExtensions = ['jpg','png','jpeg','obj']
    with zipfile.ZipFile(uploadedZip,'r') as z:
        for i in z.namelist():
            tempFileType = i.split('.')[-1]
            tempFileType = tempFileType.lower()
            if tempFileType not in validExtensions:
                return False
    return True

@login_required(login_url='login')
def uploadPage(request):
    uploadForm = UploadPackageForm()
    if request.method == 'POST':
        uploadForm = UploadPackageForm(request.POST,request.FILES)
        if uploadForm.is_valid():
            #commit=False as I understand means that it puts the content of the form in uploadedPackage without saving it to the database
            uploadedPackage = uploadForm.save(commit=False)
            uploadedPackage.packageItems = request.FILES['packageItems']
            uploadedPackage.uId = request.user
            #fileType stores the extension of the package, for later checking that it's a .zip file
            fileType = uploadedPackage.packageItems.url.split('.')[-1]
            fileType = fileType.lower()
            if fileType != 'zip' or validZip(uploadedPackage.packageItems) == False:
                return redirect('upload')
            uploadedPackage.save()
            #print("PACKAGE PATH"+uploadedPackage.packageItems.url)
            # while path.exists(uploadedPackage.packageItems.url) == False:
            #     continue
            print('package '+uploadedPackage.packageName+' saved')
            return redirect('home')
    context={'packageForm':uploadForm}
    return render(request,'users/upload.html',context)
