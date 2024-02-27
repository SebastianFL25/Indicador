# model
from rest_framework.pagination import PageNumberPagination
from base.pagination import LargeResultsSetPagination
from unit.models import EconomicIndicator
from calendar import IllegalMonthError
# serializer
from unit.api.serializers import EIModelSerializer

# django rest_framework
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
#errors
from rest_framework.exceptions import ValidationError
# json
import json
#urllib
from urllib import request
#utils
from unit.utils import generar_fechas_por_mes
from unit.utils import Mindicador
#django
from django.shortcuts import render
#utils
import json
import requests
from datetime import datetime


#CREATE OR GET THE UNITS FOR DATES OR MONTH
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create_unit(request):
    indicador = request.GET.get('indicator')
    date = request.GET.get('date')
    
    print(indicador)
    if  indicador and date:
    
        num = 1
        u_creados={}
        if len(date.split('-')) == 2:
            try:
                year,month =date.split('-')
                today = datetime.today()
                fechas_mes_actual = generar_fechas_por_mes(int(month),int(year))
                
                for fecha in fechas_mes_actual:
                    
                    name_dict = f'Unidad {num}'
                    fecha_actual = datetime.strptime(fecha, "%d-%m-%Y").strftime('%Y-%m-%d')
                    # Validate if the date already exists in the database
                    if EconomicIndicator.objects.filter(indicator=indicador,date=fecha_actual).exists():
                        
                        u_exist = EconomicIndicator.objects.get(indicator=indicador,date=fecha_actual)
                        serializer_data = EIModelSerializer(u_exist)
                    
                        u_creados[name_dict]= serializer_data.data
                        
                    else:
                        ufvalue = Mindicador(indicador=indicador, date=fecha)
                        data = ufvalue.GetValueByDate()
                        if 'error' in data:
                            # Return the error response with status code 400
                            return Response(data, status=400) 
                        if data and 'serie' in data and len(data['serie']) > 0:
                            uf_date = datetime.strptime(data['serie'][0]['fecha'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%Y-%m-%d')
                            uf_value = float(data['serie'][0]['valor'])
                            
                            u_data = {'indicator': indicador, 'date': uf_date, 'value': uf_value}
                            serializer_data = EIModelSerializer(data=u_data)
                            if serializer_data.is_valid():
                                serializer_data.save()
                                u_creados[name_dict]= serializer_data.data
                    num+=1
                        
                        
                # Return response
                return Response({"Unidades":u_creados}, status=status.HTTP_200_OK)
            except  IllegalMonthError as i:
                return Response({"message":"Format incorrect YYYY-mm"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                date_ = datetime.strptime(date, "%Y-%m-%d").strftime('%d-%m-%Y')
                ufvalue = Mindicador(indicador=indicador, date=date_)
                data = ufvalue.GetValueByDate()
                if 'error' in data:
                    # Return the error response with status code 400
                    return Response({"message":"Incorrect Format date or Indicator does'nt exist"}, status=status.HTTP_400_BAD_REQUEST) 
                else:
                    uf_date = datetime.strptime(data['serie'][0]['fecha'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%Y-%m-%d')
                    
                    uf_value = float(data['serie'][0]['valor'])
                    # Validate if the date already exists in the database
                    if EconomicIndicator.objects.filter(indicator=indicador,date=uf_date).exists():
                        u_exist = EconomicIndicator.objects.get(indicator=indicador,date=uf_date)
                        serializer_data = EIModelSerializer(u_exist)
                        message={"message":"Unidad exist","data":serializer_data.data}
                    else:
                        u_data = {'indicator': indicador, 'date': uf_date, 'value': uf_value}
                        serializer_data = EIModelSerializer(data=u_data)
                        if serializer_data.is_valid():
                            serializer_data.save()
                            message={"message":"Unidad Saved ","data":serializer_data.data}
                        else:
                            message={"message":serializer_data.errors} 
                    # Add the missing return statement
                    return Response(data=message,status=status.HTTP_200_OK)  
            except ValueError as e:
                return Response({"message":"Data does not match format , the format is YYYY-mm-dd "},status=status.HTTP_400_BAD_REQUEST)  
    return Response({"message":"Information is missing"},status=status.HTTP_400_BAD_REQUEST)      
                
    
#LIST FOR RANGE OF DATES OR MONTH
class UnitListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    serializer_class = EIModelSerializer
    queryset = EconomicIndicator.objects.all()
    
    def get_queryset(self):
        indicator = self.request.GET.get('indicator')
        date = self.request.GET.get('date')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        # Validate required fields
        if not indicator:
            raise ValidationError({'error': 'Missing required field: indicator'}, code=status.HTTP_400_BAD_REQUEST)
        
        if not date and not start_date and not end_date:
            raise ValidationError({'error': 'Missing required field: date or (start_date , end_date)'}, code=status.HTTP_400_BAD_REQUEST)
        if date:
            try:
                year, month = date.split('-')
                units = EconomicIndicator.objects.filter(indicator=indicator, date__month=month, date__year=year)
            except ValueError:
                raise ValidationError("Incorrect date format YYYY-mm")
            
        elif start_date and end_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                
                if end_date_obj < start_date_obj:
                    raise ValidationError("End date must be greater than or equal to start date")
                
                units = EconomicIndicator.objects.filter(indicator=indicator, date__range=[start_date_obj, end_date_obj]).order_by('date')
            except ValueError:
                raise ValidationError("Incorrect date format YYYY-mm-dd")
            
        else:
            units = EconomicIndicator.objects.all()
        
        return units
        

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            
            if not queryset.exists():
                return Response({"message": "Data not found , in the case not found , could finde of the value on url of obtenting data "}, status=status.HTTP_204_NO_CONTENT)
            
            paginated_queryset = self.paginate_queryset(queryset)
            if paginated_queryset is not None:
                serializer = self.get_serializer(paginated_queryset, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
