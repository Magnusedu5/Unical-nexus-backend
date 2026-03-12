import csv
import io
from django.db import transaction
from .models import Result
from unical_fees_portal.accounts.models import StudentProfile

def process_result_csv(file, course, session, semester):
    """
    Parses a CSV file and updates/creates Result objects.
    Returns a tuple: (processed_count, errors_list)
    """
    decoded_file = file.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    reader = csv.DictReader(io_string)
    
    processed_count = 0
    errors = []

    with transaction.atomic():
        for index, row in enumerate(reader):
            # Expected CSV format: matric_number, score, grade
            matric_number = row.get('matric_number')
            score = row.get('score')
            grade = row.get('grade')
            
            if not matric_number or not score:
                errors.append(f"Row {index + 1}: Missing matric_number or score")
                continue

            try:
                student_profile = StudentProfile.objects.get(matric_number=matric_number.strip())
                student = student_profile.user
                
                Result.objects.update_or_create(
                    student=student,
                    course=course,
                    session=session,
                    semester=semester,
                    defaults={'score': score, 'grade': grade}
                )
                processed_count += 1
            except StudentProfile.DoesNotExist:
                errors.append(f"Row {index + 1}: Student with matric {matric_number} not found")
    
    return processed_count, errors