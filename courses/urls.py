from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('<int:id>/', views.course_detail, name='course_detail'),
    path('<int:id>/edit/', views.course_update, name='course_update'),
    path('<int:id>/delete/', views.course_delete, name='course_delete'),

]
