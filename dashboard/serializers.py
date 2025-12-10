from rest_framework import serializers

class StatsSerializer(serializers.Serializer):
    # Champs génériques pour stats (pas lié à un model)
    total_properties = serializers.IntegerField(read_only=True)
    total_users      = serializers.IntegerField(read_only=True)
    total_bookings   = serializers.IntegerField(read_only=True)
    total_payments   = serializers.FloatField(read_only=True)  # e.g., somme des montants
    active_owners    = serializers.IntegerField(read_only=True)
    # Ajoute plus selon besoin 
    stats_by_city    = serializers.DictField(read_only=True)