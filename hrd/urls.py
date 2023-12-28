"""
URL configuration for erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from . import views
urlpatterns = [
    path('hrd_home/', views.hrd_home, name='hrd_home'),
    path('user_list/', views.user_list, name='user_list'),
    path('user_details/<int:user_id>/', views.user_details, name='user_details'),
    # path('user_details/<int:user_id>/', UserDetailsView.as_view(), name='user_details'),
    path('create_employee/', views.create_employee, name='create_employee'),
    path('create_department/', views.create_department, name='create_department'),
    path('create_position/', views.create_position, name='create_position'),
    path('create_document_type/', views.create_document_type, name='create_document_type'),
    path('create_document/', views.create_document, name='create_document'),
    path('add_documents_to_employee/<int:employee_id>/', views.add_documents_to_employee, name='add_documents_to_employee'),
]
