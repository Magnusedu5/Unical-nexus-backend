from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, StudentProfile, StaffProfile, AdminProfile

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizes the JWT response to include user's role, id, and full name.
    """
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role
        token['user_id'] = user.id
        token['full_name'] = user.get_full_name()
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add user role, id, and full name to the response
        data['user_role'] = self.user.role
        data['user_id'] = self.user.id
        data['full_name'] = self.user.get_full_name()
        
        # The default response returns access and refresh tokens.
        # We are renaming 'access' to 'access_token' and 'refresh' to 'refresh_token'.
        data['access_token'] = data.pop('access')
        data['refresh_token'] = data.pop('refresh')

        return data

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['matric_number', 'faculty', 'department', 'level']

class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = ['staff_id', 'department']

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ['staff_id', 'department']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    student_profile = StudentProfileSerializer(required=False)
    staff_profile = StaffProfileSerializer(required=False)
    admin_profile = AdminProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password', 'student_profile', 'staff_profile', 'admin_profile']

    def create(self, validated_data):
        student_data = validated_data.pop('student_profile', None)
        staff_data = validated_data.pop('staff_profile', None)
        admin_data = validated_data.pop('admin_profile', None)
        # create_user takes password as a separate argument
        password = validated_data.pop('password')
        
        user = User.objects.create_user(**validated_data, password=password)

        if user.role == User.Roles.STUDENT and student_data:
            StudentProfile.objects.create(user=user, **student_data)
        elif user.role == User.Roles.STAFF and staff_data:
            StaffProfile.objects.create(user=user, **staff_data)
        elif user.role == User.Roles.ADMIN and admin_data:
            AdminProfile.objects.create(user=user, **admin_data)
            
        return user