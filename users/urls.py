from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('login/',views.loginPage,name="login"),
    path('register/',views.registerPage,name="register")
]