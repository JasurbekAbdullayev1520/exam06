# students/urls.py
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # Main CRUD
    path('', views.StudentListView.as_view(), name='student_list'),
    path('create/', views.StudentCreateView.as_view(), name='student_create'),
    path('<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('<int:pk>/update/', views.StudentUpdateView.as_view(), name='student_update'),
    path('<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),
    
    # Documents
    path('<int:pk>/document/upload/', views.student_document_upload, name='document_upload'),
    path('<int:pk>/document/<int:doc_id>/delete/', views.student_document_delete, name='document_delete'),
    
    # Export
    path('export/excel/', views.export_students_excel, name='export_excel'),
    
    # Bulk Actions
    path('bulk-action/', views.bulk_action, name='bulk_action'),
    
    # Statistics
    path('statistics/', views.student_statistics, name='statistics'),
    
    # AJAX endpoints
    path('api/check-email/', views.check_email_availability, name='check_email'),
    path('api/quick-search/', views.student_quick_search, name='quick_search'),
]