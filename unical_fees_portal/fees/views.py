import uuid
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import FeeItem, FacultyCharge, ExtraCharge, Payment, Transaction
from .serializers import (
    FeeItemSerializer, FacultyChargeSerializer, ExtraChargeSerializer, 
    PaymentSerializer, TransactionSerializer,
    PaymentInitializeSerializer, PaymentVerifySerializer
)
from unical_fees_portal.accounts.permissions import IsAdmin, IsStudent

class FeeItemViewSet(viewsets.ModelViewSet):
    queryset = FeeItem.objects.all()
    serializer_class = FeeItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class FacultyChargeViewSet(viewsets.ModelViewSet):
    queryset = FacultyCharge.objects.all()
    serializer_class = FacultyChargeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExtraChargeViewSet(viewsets.ModelViewSet):
    queryset = ExtraCharge.objects.all()
    serializer_class = ExtraChargeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'head']

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'ADMIN' or user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(student=user)

    @action(detail=False, methods=['post'])
    def initialize(self, request):
        serializer = PaymentInitializeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        amount = serializer.validated_data['amount']
        description = serializer.validated_data['description']
        user = request.user
        
        reference = f"REF-{uuid.uuid4().hex[:12].upper()}"
        
        Payment.objects.create(
            student=user,
            amount=amount,
            reference=reference,
            description=description,
            status='PENDING'
        )
        
        return Response({
            'status': 'success',
            'message': 'Payment initialized',
            'data': {
                'reference': reference,
                'authorization_url': f"https://checkout.dummy-payment.com/pay/{reference}?amount={amount}",
                'access_code': uuid.uuid4().hex
            }
        })

    @action(detail=False, methods=['post'])
    def verify(self, request):
        serializer = PaymentVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        reference = serializer.validated_data['reference']
        
        try:
            payment = Payment.objects.get(reference=reference)
            if getattr(request.user, 'role', None) == 'STUDENT' and payment.student != request.user:
                 return Response({'status': 'error', 'message': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Payment.DoesNotExist:
            return Response({'status': 'error', 'message': 'Invalid payment reference'}, status=status.HTTP_404_NOT_FOUND)
            
        if payment.status == 'SUCCESS':
            return Response({'status': 'success', 'message': 'Payment already verified'})
            
        # Mock verification logic
        payment.status = 'SUCCESS'
        payment.save()
        
        Transaction.objects.create(
            payment=payment,
            description=f"Verified payment: {payment.description or payment.reference}"
        )
        
        return Response({
            'status': 'success',
            'message': 'Payment verification successful',
            'data': PaymentSerializer(payment).data
        })

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'ADMIN' or user.is_staff:
            return Transaction.objects.all()
        return Transaction.objects.filter(payment__student=user)