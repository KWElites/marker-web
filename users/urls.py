from django.urls import path
from django.urls.resolvers import URLPattern
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.static import serve
from . import views

urlpatterns = [
    path('',views.homePage,name="home"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('profile/<username>',views.profilePage,name="profile"),
    path('upload/',views.uploadPage,name="upload"),
    path('editprofile/',views.editProfile,name="editprofile"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        })
    ]
