from django.urls import path
from . import views

urlpatterns = [
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_create, name='employee_add'),
    path('employees/<str:pk>/', views.employee_detail, name='employee_detail'),
]