from rest_framework import serializers
from django.db import transaction
from unical_fees_portal.accounts.models import User, StaffProfile

class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = ['staff_id', 'department']

class StaffSerializer(serializers.ModelSerializer):
    profile = StaffProfileSerializer(source='staff_profile')
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'profile']
    
    def create(self, validated_data):
        profile_data = validated_data.pop('staff_profile')
        password = validated_data.pop('password')
        
        with transaction.atomic():
            user = User.objects.create_user(
                password=password, 
                role=User.Roles.STAFF,
                **validated_data
            )
            StaffProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('staff_profile', None)
        
        # Update User fields
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        # Update Profile fields
        if profile_data:
            profile, created = StaffProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
            
        return instance