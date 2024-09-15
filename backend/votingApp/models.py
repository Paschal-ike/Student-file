from django.db import models
from django.contrib.auth.models import AbstractUser

# User model inheriting from AbstractUser with an is_admin flag
class AppUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
     # Add unique related_name attributes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='appuser_set',
        related_query_name='appuser'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='appuser_set',
        related_query_name='appuser'
    )
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
# Student model to store student details


# Upload model to track the file uploads and their status
class Upload(models.Model):
    file_name = models.CharField(max_length=255)  # Name of the file uploaded
    status = models.CharField(max_length=20, choices=[('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')])
    uploaded_at = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return f'{self.file_name} ({self.status})'

class Student(models.Model):
    upload = models.ForeignKey(Upload, related_name='students', on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.CharField(max_length=30, unique=True)  # Unique student ID
    first_name = models.CharField(max_length=100)  
    last_name = models.CharField(max_length=100)  
    email = models.EmailField()  
    department = models.CharField(max_length=100)  
    faculty = models.CharField(max_length=100, blank=True, null=True)  
    uploaded_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
