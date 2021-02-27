from django.contrib import admin
from django.urls import path, include
from employee import views

urlpatterns = [
	path('add_employee', views.add_employee, name='add-employee'),
	path('add_department', views.add_department, name='add-department'),
]
