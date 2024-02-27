# Rest Framework 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
#Django
from django.contrib.auth import authenticate
#Serializers
from .serializers import UsuarioSerializer,CustomTokenObtainPairSerializer
#Models
from base.models import *

#Create User
class UsuarioCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Obtain Token
class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        
        
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                refresh = RefreshToken.for_user(user)
                access_token = serializer.validated_data['access']
                
                user_data = UsuarioSerializer(user).data
                
                return Response({
                    "user": user_data,
                    **serializer.validated_data,
                })
        raise AuthenticationFailed("Credenciales inválidas")
    
#Refresh
class refresh(TokenRefreshView):
    pass

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()  # Obtén todos los usuarios autenticados
    serializer_class = UsuarioSerializer  # Serializa los usuarios
    permission_classes = [IsAuthenticated]
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    if request.method == 'GET':
        queryset = CustomUser.objects.all()  # Obtén todos los usuarios autenticados
        serializer = UsuarioSerializer(queryset, many=True)  # Serializa los usuarios
        return Response(serializer.data)