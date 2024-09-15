import os
import pandas as pd
from .models import Student, Upload
from django.core.mail import send_mail
from django.conf import settings
import dramatiq

import logging
logger = logging.getLogger(__name__)

@dramatiq.actor
def process_file_task(file_path):
    file_name = os.path.basename(file_path)
    logger.info(f"Starting to process file: {file_name}")

    try:
        # Determine file type
        if file_name.endswith('.csv'):
            data = pd.read_csv(file_path)
            logger.debug(f"Loaded CSV file: {file_name}")
        elif file_name.endswith('.xlsx'):
            data = pd.read_excel(file_path)
            logger.debug(f"Loaded Excel file: {file_name}")
        else:
            raise ValueError("Unsupported file format")

        processed_records = 0
        students_to_create = []
        students_to_update = []

         # Retrieve the Upload instance
        upload = Upload.objects.get()
        
        for _, row in data.iterrows():
            if pd.isna(row['student_id']) or pd.isna(row['first_name']) or pd.isna(row['email']):
                logger.warning(f"Skipping row with missing required fields: {row}")
                continue

            student_data = {
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'department': row.get('department', ''),
                'faculty': row.get('faculty', ''),
                "upload" : upload,
            }

            try:
                student = Student.objects.get(student_id=row['student_id'])
                for key, value in student_data.items():
                    setattr(student, key, value)
                students_to_update.append(student)
                logger.info(f"Updated student: {student.student_id}")
            except Student.DoesNotExist:
                students_to_create.append(Student(student_id=row['student_id'], **student_data))
                logger.info(f"Created new student: {row['student_id']}")

            processed_records += 1
            

        # Bulk operations
        if students_to_create:
            Student.objects.bulk_create(students_to_create)
            logger.info(f"Created {len(students_to_create)} new students")
        if students_to_update:
            Student.objects.bulk_update(students_to_update, ['first_name', 'last_name', 'email', 'department', 'faculty'])
            logger.info(f"Updated {len(students_to_update)} students")

        # Notify admin
        send_mail(
            f'Student Voter Data Processed: {file_name}',
            f'{processed_records} student records were saved.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        logger.info(f"File processing complete: {file_name}")

    except Exception as e:
        logger.error(f"Error processing file {file_name}: {str(e)}", exc_info=True)
        send_mail(
            f'Error Processing Student Voter Data: {file_name}',
            f'An error occurred: {str(e)}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted file after processing: {file_name}")
