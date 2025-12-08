from rest_framework import serializers
from .models import ContractTemplate, Contract

class ContractTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractTemplate
        fields = ['id', 'created_by', 'title', 'content']

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'template', 'property', 'owner', 'tenant', 'start_date', 'end_date', 'amount', 'signed_by_owner', 'signed_by_tenant', 'pdf_file', 'created_at']