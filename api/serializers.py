from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Faculty, Department, Programme, Course, Student, Result, FeeItem, Session, Semester, Report

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Rename default keys to match frontend expectation
        data['access_token'] = data.pop('access')
        data['refresh_token'] = data.pop('refresh')
        
        # Add user details
        data['user_id'] = self.user.id
        data['full_name'] = self.user.get_full_name() or self.user.username
        
        # Determine role based on Django permissions (Placeholder logic)
        if self.user.is_superuser:
            data['user_role'] = 'ADMIN'
        elif self.user.is_staff:
            data['user_role'] = 'STAFF'
        else:
            data['user_role'] = 'STUDENT'
            
        return data

class FacultySerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Faculty
        fields = ['id', 'name', 'createdAt']

class DepartmentSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    # Maps the 'faculty' model field to 'faculty_id' in JSON for both read and write
    faculty_id = serializers.PrimaryKeyRelatedField(
        source='faculty', queryset=Faculty.objects.all()
    )
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'faculty_id', 'faculty_name', 'created_at']

class ProgrammeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    # Maps the 'department' model field to 'department_id' in JSON for both read and write
    department_id = serializers.PrimaryKeyRelatedField(
        source='department', queryset=Department.objects.all()
    )

    class Meta:
        model = Programme
        fields = ['id', 'name', 'department_id', 'department_name', 'created_at']

class CourseSerializer(serializers.ModelSerializer):
    programme_name = serializers.CharField(source='programme.name', read_only=True)
    programme_id = serializers.PrimaryKeyRelatedField(
        source='programme', queryset=Programme.objects.all()
    )

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'programme_id', 'programme_name', 'created_at']

class StudentSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        source='department', queryset=Department.objects.all()
    )

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'matric_number', 'department_id', 'department_name', 'created_at']

class ResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    student_matric = serializers.CharField(source='student.matric_number', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    student_id = serializers.PrimaryKeyRelatedField(
        source='student', queryset=Student.objects.all()
    )
    course_id = serializers.PrimaryKeyRelatedField(
        source='course', queryset=Course.objects.all()
    )

    class Meta:
        model = Result
        fields = ['id', 'student_id', 'student_name', 'student_matric', 'course_id', 'course_code', 'course_name', 'score', 'grade', 'created_at']

class FeeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeItem
        fields = ['id', 'name', 'description', 'amount', 'created_at']

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'name', 'start_date', 'end_date', 'created_at']

class SemesterSerializer(serializers.ModelSerializer):
    session_name = serializers.CharField(source='session.name', read_only=True)
    session_id = serializers.PrimaryKeyRelatedField(
        source='session', queryset=Session.objects.all()
    )

    class Meta:
        model = Semester
        fields = ['id', 'name', 'session_id', 'session_name', 'start_date', 'end_date', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'title', 'description', 'data', 'generated_at']