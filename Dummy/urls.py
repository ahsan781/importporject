"""Dummy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from os import name
from django.contrib import admin
from django.urls import path
from website import views
from django.contrib.auth import login, views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.csvDisplay),
    path('editCsv/', views.editCsv, name='editCsv'),
    path('Row/<int:rowNum>', views.changeRow , name='Row'),
    path('delete/<int:rowNum>', views.deleteRow, name='delete'),
    path('discardFile', views.discardFile, name='discardFile'),
    path('saveCsvFile', views.saveCsvFile, name='saveCsvFile'),
    path('displayUserCSV', views.displayUserCSV, name='displayUserCSV'),
    path('updateCSVFile/<str:fname>', views.updateCSVFile, name='updateCSVFile'),
    path('csvdata', views.csvdata, name='csvdata'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html',redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

 
    # Testing
    # path('value_test/<int:num1>/<int:num2>', views.value_test, name='value_test'),
    # path('redirecting', views.redirecting, name='redirecting'),

]
