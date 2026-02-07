from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizes the JWT response to include user's role, id, and full name.
    """
    username_field = 'email'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields.pop('username', None)
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