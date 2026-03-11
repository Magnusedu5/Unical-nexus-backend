from rest_framework import serializers
from .models import HostelRequest, Hostel

class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = '__all__'

class HostelRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_matric = serializers.CharField(source='student.student_profile.matric_number', read_only=True)
    hostel_details = HostelSerializer(source='hostel', read_only=True)

    class Meta:
        model = HostelRequest
        fields = '__all__'
        read_only_fields = ['status', 'student', 'comment']

class HostelStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelRequest
        fields = ['status', 'comment']