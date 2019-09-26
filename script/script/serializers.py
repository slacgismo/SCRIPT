from rest_framework import serializers
from script.models import AlgorithmA

# serializer of result model
class AlgorithmASerializer(serializers.ModelSerializer):
    class Meta:
        model = AlgorithmA
        fields = '__all__'
