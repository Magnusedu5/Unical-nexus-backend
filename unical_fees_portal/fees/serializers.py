from rest_framework import serializers
from .models import FeeItem, FacultyCharge, ExtraCharge, Payment, Transaction

class FeeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeItem
        fields = '__all__'

class FacultyChargeSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = FacultyCharge
        fields = '__all__'

class ExtraChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraCharge
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'

class PaymentInitializeSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(max_length=255)
    fee_item_id = serializers.UUIDField(required=False)

class PaymentVerifySerializer(serializers.Serializer):
    reference = serializers.CharField(max_length=100)

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'