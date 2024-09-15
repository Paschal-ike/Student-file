from django.urls import path
from .admin_views import AdminRegisterView, AdminLoginView, RefreshTokenView
from  .students_view import StudentListCreateView, StudentDetailView, StudentFileUploadView, UploadListView, UploadDetailView



urlpatterns = [
    path('admin/register/', AdminRegisterView.as_view(), name='admin-register'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('refresh-token/', RefreshTokenView.as_view(), name='token-refresh'),


    # Student endpoints
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('students/upload/', StudentFileUploadView.as_view(), name='student-upload'),
    path('students/<student_id>/', StudentDetailView.as_view(), name='student-detail'),
    
    path('uploads/', UploadListView.as_view(), name='upload-list'),
    path('uploads/<int:pk>/', UploadDetailView.as_view(), name='upload-detail'),

]
