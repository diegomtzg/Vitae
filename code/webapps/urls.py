"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vitae import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.searchAction, name='search'),
    path('register/', views.registerAction, name='register'),
    path('login/', views.loginAction, name='login'),
    path('photos/<str:username>/', views.getPhoto, name='photo'),
    path('profile/<str:username>/', views.visitProfileAction, name='profile'),
    path('profile/<str:username>/edit/<str:sectionName>/', views.editProfile, name='editProfile'), # TODO: What if username is 'something/edit'? Need to check usernames
    # TODO: Also handle profile editing (currently just adding elements): need /profile/edit/section/elementId

    path('logout', views.debugLogout),
    path('delete', views.debugDelete),
]
