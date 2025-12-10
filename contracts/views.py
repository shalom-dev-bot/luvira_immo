from rest_framework import viewsets, permissions
from rest_framework.response import Response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from rest_framework.decorators import action
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

    @action(detail=True, methods=['get'], url_path='generate-pdf')
    def generate_pdf(self, request, pk=None):
        contract = self.get_object()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="contrat_{contract.id}.pdf"'
        p = canvas.Canvas(response, pagesize=letter)
        p.drawString(100, 750, f"Contrat de Bail n° {contract.id}")
        p.drawString(100, 730, f"Propriétaire: {contract.owner.username}")
        p.drawString(100, 710, f"Locataire: {contract.tenant.username}")
        p.drawString(100, 690, f"Bien: {contract.property.title}")
        p.drawString(100, 670, f"Montant: {contract.amount} FCFA")
        p.drawString(100, 650, f"Dates: {contract.start_date} à {contract.end_date}")
        p.drawString(100, 600, "Clauses :")
        p.drawString(100, 580, contract.template.content if contract.template else "Clauses standards")  # Contenu template
        p.drawString(100, 500, "Signature Propriétaire: " + ("Signé" if contract.signed_by_owner else "En attente"))
        p.drawString(100, 480, "Signature Locataire: " + ("Signé" if contract.signed_by_tenant else "En attente"))
        p.save()
        # Sauvegarde PDF dans model (optionnel, ou envoi email)
        contract.pdf_file.save(f"contrat_{contract.id}.pdf", response)
        contract.save()
        return response  # Télécharge PDF