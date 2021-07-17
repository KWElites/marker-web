from users.handlers.validator import validZip
from marker import settings
from users.handlers.package_handler import extractPackage, generatePackageQRCode, getPackageItems
from users.models import Package, UserProfile, Store
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, ProfileForm, UploadPackageForm, StoreForm
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
    context = {}
    packages = Package.objects.order_by('-id')[:2]
    context["packages"] = packages

    if request.method == 'POST' and request.POST.get('searchBarText') != "":
        searchText = request.POST.get('searchBarText')
        userProfiles = UserProfile.objects.filter(name__contains=searchText)
        
        packages = Package.objects.filter(packageName__contains=searchText)
        for profile in userProfiles:
            packages|=(Package.objects.filter(uId_id=profile.user_id))
        context["packages"] = packages
    if request.user.is_authenticated:
        user = request.user
        userProfile = UserProfile.objects.get(user_id = user.id)
        context["userP"] = userProfile

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
    storeForm = StoreForm()
    if request.method == 'POST':
        uploadForm = UploadPackageForm(request.POST,request.FILES)
        storeForm = StoreForm(request.POST)
        if uploadForm.is_valid() and storeForm.is_valid():
            #commit=False as I understand means that it puts the content of the form in uploadedPackage without saving it to the database
            uploadedStore = Store(uId = request.user, storeName = storeForm.cleaned_data.get('storeName'))
            uploadedStore.save()
            
            uploadedPackage = uploadForm.save(commit = False)
            uploadedPackage.packageItems = request.FILES['packageItems']
            uploadedPackage.uId = request.user
            uploadedPackage.sId = uploadedStore
             
            
            #fileType stores the extension of the package, for later checking that it's a .zip file
            fileType = uploadedPackage.packageItems.url.split('.')[-1]
            fileType = fileType.lower()
            
            if fileType != 'zip' or validZip(uploadedPackage.packageItems) == False:
                return redirect('upload')
            
            uploadedPackage.save()

            #print(uploadedPackage.packageItems.url)
            extractPackage(uploadedPackage)
            print('package '+uploadedPackage.packageName+' saved')
            return redirect('home')
    
    context={
        'packageForm' : uploadForm,
        'storeForm' : storeForm
    }
    return render(request, 'users/upload.html', context)

@login_required(login_url='login')
def packageViewPage(request, pk):
    user = request.user
    package = Package.objects.get(uId = user.id, id = pk)
    package_items = getPackageItems(package.packageItems, package.packageImages)
    store = Store.objects.get(uId = user.id, id = package.sId.id)
    qr_code = generatePackageQRCode(request.get_host(), package.packageItems.url)
    
    context={
        'user': user,
        'package': package,
        'package_items': package_items,
        'media_url': settings.MEDIA_URL,
        'store': store,
        'qr_code': qr_code
    }
    return render(request, 'users/viewpackage.html', context)