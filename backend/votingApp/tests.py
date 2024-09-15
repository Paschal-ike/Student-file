from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Student
import os
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class AdminViewTests(APITestCase):
    def setUp(self):
        # Create an admin user
        self.admin = User.objects.create_user(username='admin', email='admin@test.com', password='admin123', is_admin=True)
    
    def test_admin_registration(self):
        url = reverse('admin-register')
        data = {'username': 'newadmin', 'email': 'newadmin@test.com', 'password': 'adminpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Admin created successfully', response.data['message'])

    def test_admin_registration_invalid(self):
        url = reverse('admin-register')
        data = {'username': '', 'email': 'bademail', 'password': 'adminpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('VALIDATION_ERROR', response.data['error_code'])

    def test_admin_login(self):
        url = reverse('admin-login')
        data = {'username': 'admin', 'password': 'admin123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_admin_login_invalid(self):
        url = reverse('admin-login')
        data = {'username': 'admin', 'password': 'wrongpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Invalid credentials provided', response.data['error'])

    def test_admin_list(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('admin-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class StudentViewTests(APITestCase):
    def setUp(self):
        # Create a student record
        self.student = Student.objects.create(student_id='S001', first_name='John', last_name='Doe', email='john.doe@test.com', department='Engineering')

    def test_list_students(self):
        url = reverse('student-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_student(self):
        url = reverse('student-list-create')
        data = {
            'student_id': 'S002',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@test.com',
            'department': 'Science'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['student_id'], 'S002')

    def test_upload_file(self):
        url = reverse('student-upload')
        file_path = os.path.join(os.path.dirname(__file__), 'test_file.csv')
        file = SimpleUploadedFile('test_file.csv', b'student_id,first_name,last_name,email,department\nS003,Test,User,test.user@test.com,Law')
        response = self.client.post(url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_upload_invalid_file(self):
        url = reverse('student-upload')
        file = SimpleUploadedFile('test_file.txt', b'Invalid content')
        response = self.client.post(url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('INVALID_FILE_FORMAT', response.data['error_code'])

    def test_student_detail(self):
        url = reverse('student-detail', args=[self.student.student_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student_id'], 'S001')

    def test_update_student(self):
        url = reverse('student-detail', args=[self.student.student_id])
        data = {'first_name': 'UpdatedName'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'UpdatedName')

    def test_delete_student(self):
        url = reverse('student-detail', args=[self.student.student_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(student_id='S001').exists())
