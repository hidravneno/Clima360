from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.conf import settings
from django.shortcuts import render

#Base html para inicio 
def home(request):
    return render(request, 'home.html')

#Para saber el clima actualmente
class CurrentWeatherView(APIView):
    def get(self, request):
        city = request.GET.get('city')
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')

        api_key = settings.OPENWEATHER_API_KEY
        if city:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        else:
            url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'

        data = requests.get(url).json()
        return Response({
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        })

#Para saber el clima en los proximos dias
class ForecastWeatherView(APIView):
    def get(self, request):
        city = request.GET.get('city')
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        api_key = settings.OPENWEATHER_API_KEY

        if city:
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
        else:
            url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric'

        data = requests.get(url).json()
        return Response(data)

#Para buscar el clima de ciudades
class CitySearchView(APIView):
    def get(self, request):
        query = request.GET.get('q')
        api_key = settings.OPENWEATHER_API_KEY

        if not query:
            return Response({"error": "Falta parámetro ?q="}, status=400)

        url = f'http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={api_key}'
        data = requests.get(url).json()
        return Response(data)

#Para saber si hay alertas meteorologicas 
class WeatherAlertsView(APIView):
    def get(self, request):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        api_key = settings.OPENWEATHER_API_KEY

        if not lat or not lon:
            return Response({"error": "Se requieren lat y lon"}, status=400)

        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily,current&appid={api_key}"
        data = requests.get(url).json()

        alerts = data.get("alerts", [])
        return Response({"alerts": alerts})

