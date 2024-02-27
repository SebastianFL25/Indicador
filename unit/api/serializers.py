from unit.models import EconomicIndicator

# restframework
from rest_framework import serializers


class EIModelSerializer(serializers.ModelSerializer):
    #date = serializers.DateField()
    #value = serializers.FloatField()

    
    def create(self, validated_data):
        return EconomicIndicator.objects.create(**validated_data)
    
   
    
    class Meta:
        model = EconomicIndicator
        fields = ('indicator','date','value')