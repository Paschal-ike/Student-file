from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView,RetrieveUpdateDestroyAPIView

from .tasks import process_file_task
from .models import Student, Upload
from .serializers import StudentSerializer, UploadSerializer
from .permissions import IsAdminUser
from .utils import format_error_response, save_file_to_disk

class StudentFileUploadView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only admins can access this

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response(
                format_error_response(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    error_code='no_file_provided',
                    message='No file provided.'
                ), 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create an Upload model instance
        upload = Upload(file_name=file.name, status='processing')
        upload.save()

        # Save the file to disk temporarily
        file_path = save_file_to_disk(file)
        
        # Trigger the asynchronous task to process the file
        process_file_task.send(file_path)

        # Serialize the Upload instance and return the response
        serializer = UploadSerializer(upload)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class StudentListCreateView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Only admins can access this
    
    def perform_create(self, serializer):
        # Add custom logic here before saving if needed
        serializer.save()

class StudentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class UploadListView(ListCreateAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


    



class UploadDetailView(RetrieveAPIView):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        upload = self.get_object()
        data = {
            'upload': UploadSerializer(upload).data,
            'students': StudentSerializer(Student.objects.filter(upload=upload), many=True).data
        }
        return Response(data)
