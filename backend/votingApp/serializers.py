from rest_framework import serializers
from .models import Student, Upload
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password


AppUser = get_user_model()

class AdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = AppUser
        fields = ('username', 'email', 'password', 'password2')

    # Validate that passwords match
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields do not match."})
        return data

    def create(self, validated_data):
        # Remove password2 before saving
        validated_data.pop('password2')
        user = AppUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_admin=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class AdminLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        return {'user': user}


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'email', 'department', 'faculty', 'uploaded_at']

    # Custom validation for student fields
    def validate_email(self, value):
        if Student.objects.filter(email=value).exists():
            raise serializers.ValidationError("A student with this email already exists.")
        return value
    
    # Validate the student_id uniqueness
    def validate_student_id(self, value):
        if Student.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("A student with this ID already exists.")
        return value

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['file_name', 'status', 'uploaded_at', 'students']

    # Validate file format
    def validate_file_name(self, value):
        if not (value.endswith('.csv') or value.endswith('.xlsx')):
            raise serializers.ValidationError("Only CSV and XLSX files are supported.")
        return value
