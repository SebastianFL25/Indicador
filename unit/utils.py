#urllib
import calendar
from urllib import request

#datetime
import datetime

#requests
import requests

# json
import json

# model
from .models import EconomicIndicator
#ssl
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# rest_framework
from rest_framework.response import Response

#CLASS MI INDICADOR
class Mindicador:
 
    def __init__(self, indicador, year =None,date =None):
        self.indicador = indicador
        self.year = year
        self.date= date
    
    def InfoApi(self):
        # In this case we make the request for the case of consulting an indicator in a certain year
        url = f'https://mindicador.cl/api/{self.indicador}/{self.year}'
        response = requests.get(url)
        data = json.loads(response.text.encode("utf-8"))
        # To make the json look neat, return pretty_json
        pretty_json = json.dumps(data, indent=2)
        return data
    
    """Get uf value by date"""
    def GetValueByDate(self):
        url = f'https://mindicador.cl/api/{self.indicador}/{self.date}'
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text.encode("utf-8"))
            # To make the json look neat, return pretty_json
            pretty_json = json.dumps(data, indent=2)
            return data
        else:
            return {"error": f"Failed to retrieve data. Status code: {response.status_code}"}
       
def generar_fechas_por_mes(mes, anio):
    _, num_dias = calendar.monthrange(anio, mes)
    fechas = [f'{dia}-{str(mes).zfill(2)}-{str(anio).zfill(2)}' for dia in range(1, num_dias+1)]
    return fechas

    
