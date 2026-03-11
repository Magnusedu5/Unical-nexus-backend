from rest_framework import serializers
from .models import PortalSettings

class PortalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortalSettings
        fields = '__all__'