from users.models import Packages, UserProfile
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, ProfileForm, UploadPackageForm

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
    context={}
    return render(request,'users/viewprofile.html',context)

@login_required(login_url='login')
def uploadPage(request):
    uploadForm = UploadPackageForm()
    print('trace -1')
    if request.method == 'POST':
        print('trace 0')
        uploadForm = UploadPackageForm(request.POST,request.FILES)
        if uploadForm.is_valid():
            print('trace 1')
            uploadedPackage = uploadForm.save(commit=False)
            #package = Packages(uId=request.user.id,packageName = uploaded_package.cleaned_data.get('packageName'), packageDesc = uploaded_package.cleaned_data.get('packageDesc'), packageThumbnail=uploaded_package.cleaned_data.get('packageThumbnail'), packageItems = uploaded_package.cleaned_data.get('packageItems'))
            uploadedPackage.packageItems = request.FILES['packageItems']
            uploadedPackage.uId = request.user
            print('trace 2')
            fileType = uploadedPackage.packageItems.url.split('.')[-1]
            fileType = fileType.lower()
            print('trace 3')
            if fileType != 'zip':
                return redirect('upload')
            print('trace 4')
            uploadedPackage.save()
            print('package '+uploadedPackage.packageName+' saved')
            return redirect('home')
    context={'packageForm':uploadForm}
    return render(request,'users/upload.html',context)