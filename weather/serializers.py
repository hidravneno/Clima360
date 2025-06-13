from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SearchHistory

# Serializers para la API de clima

# user serializer sirve para manejar la información del usuario
# y SearchHistorySerializer para manejar el historial de búsqueda del clima
# Estos serializers permiten validar y serializar los datos de los modelos 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'is_staff']
        read_only_fields = ['is_staff']  # Protege campos sensibles


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = '__all__'

    def validate_city(self, value):
        if "<script>" in value:
            raise serializers.ValidationError("Contenido no permitido")
        return value
