from rest_framework import serializers
from .models import Faculty, Department

class FacultySerializer(serializers.ModelSerializer):
    # Frontend expects 'createdAt' (camelCase)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Faculty
        fields = ['id', 'name', 'createdAt']

class DepartmentSerializer(serializers.ModelSerializer):
    # Frontend expects 'faculty_name' for display and 'faculty_id' for linking
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    
    # Map 'faculty_id' from payload to the 'faculty' ForeignKey
    faculty_id = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), source='faculty'
    )

    class Meta:
        model = Department
        fields = ['id', 'name', 'faculty_id', 'faculty_name', 'created_at']