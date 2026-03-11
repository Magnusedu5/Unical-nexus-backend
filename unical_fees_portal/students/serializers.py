from rest_framework import serializers
from django.db import transaction
from unical_fees_portal.accounts.models import User, StudentProfile

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['matric_number', 'faculty', 'department', 'level']

class StudentSerializer(serializers.ModelSerializer):
    profile = StudentProfileSerializer(source='student_profile')
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'profile']
    
    def create(self, validated_data):
        profile_data = validated_data.pop('student_profile')
        password = validated_data.pop('password')
        
        with transaction.atomic():
            user = User.objects.create_user(
                password=password,
                role=User.Roles.STUDENT,
                **validated_data
            )
            StudentProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('student_profile', None)
        
        # Update User fields
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        # Update Profile fields
        if profile_data:
            # Ensure profile exists before updating
            profile, created = StudentProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
            
        return instance