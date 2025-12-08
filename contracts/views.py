from rest_framework import viewsets, permissions
from .models import ContractTemplate, Contract
from .serializers import ContractTemplateSerializer, ContractSerializer

class ContractTemplateViewSet(viewsets.ModelViewSet):
    queryset = ContractTemplate.objects.all()
    serializer_class = ContractTemplateSerializer
    permission_classes = [permissions.IsAdminUser]  # Seul admin gère templates

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Contract.objects.all()
        elif user.role == 'owner':
            return Contract.objects.filter(owner=user)
        elif user.role == 'client':
            return Contract.objects.filter(tenant=user)
        return Contract.objects.none()