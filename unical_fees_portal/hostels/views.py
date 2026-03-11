from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import HostelRequest, Hostel
from .serializers import HostelRequestSerializer, HostelStatusUpdateSerializer, HostelSerializer
from unical_fees_portal.accounts.permissions import IsAdmin

class HostelViewSet(viewsets.ModelViewSet):
    """
    Manage the list of available hostels.
    """
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class HostelRequestViewSet(viewsets.ModelViewSet):
    """
    Manage student hostel requests.
    """
    queryset = HostelRequest.objects.all()
    serializer_class = HostelRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'ADMIN' or user.is_staff:
            return HostelRequest.objects.all()
        return HostelRequest.objects.filter(student=user)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAuthenticated, IsAdmin])
    def status(self, request, pk=None):
        """
        Custom action to update the status of a hostel request.
        Expected payload: {"status": "APPROVED" | "REJECTED", "comment": "Optional"}
        """
        hostel_request = self.get_object()
        serializer = HostelStatusUpdateSerializer(hostel_request, data=request.data, partial=True)
        
        if serializer.is_valid():
            new_status = serializer.validated_data.get('status')
            if new_status not in ['APPROVED', 'REJECTED']:
                 return Response({"error": "Invalid status. Use APPROVED or REJECTED."}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
