from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# Get our User model instead of the default one provided
Usuario = get_user_model()

# Serializer for obtaining a token using username and password
class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = Usuario.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = Usuario
        fields = [ 'username', 'email', 'password']
        
# Serialize JWT Tokens
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass