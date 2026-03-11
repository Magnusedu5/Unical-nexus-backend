from rest_framework import serializers
from .models import Result

class ResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    matric_number = serializers.CharField(source='student.student_profile.matric_number', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Result
        fields = '__all__'

class ResultUploadSerializer(serializers.Serializer):
    course_id = serializers.UUIDField(required=True)
    session = serializers.CharField(max_length=20, required=True)
    semester = serializers.CharField(max_length=20, required=True)
    file = serializers.FileField(required=True)
    
    class Meta:
        fields = ['course_id', 'session', 'semester', 'file']