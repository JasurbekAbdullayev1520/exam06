from django.urls import path
from . import views

app_name = 'enrollments'

urlpatterns = [
    path('', views.enrollment_list, name='enrollment_list'),     
    path('create/', views.enrollment_create, name='enrollment_create'), 
    path('<int:id>/edit/', views.enrollment_update, name='enrollment_update'),  
    path('<int:id>/delete/', views.enrollment_delete, name='enrollment_delete'),  
]
