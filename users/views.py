from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

# Create your views here.
def loginPage(request):
    context = {}
    return render(request,'users/login.html',context)

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            print("success")


    context = {'form':form}
    return render(request,'users/register.html',context)