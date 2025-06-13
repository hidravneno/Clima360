from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from decouple import config
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.contrib.auth.decorators import login_required
from .models import SearchHistory
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from .permissions import IsOwnerOrReadOnly
from .serializers import SearchHistorySerializer
from rest_framework import generics


permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

#Base html para inicio 
def home(request):
    return render(request, 'home.html')

#Para saber el clima actualmente
class CurrentWeatherView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]# Permite acceso a usuarios autenticados o no autenticados los no autenticados solo pueden ver el clima actual y sin historial
    def get(self, request):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        city = request.GET.get('city')

        api_key = config("OPENWEATHER_API_KEY")

        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es"
        elif lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es"
        else:
            return Response({"error": "Debe proporcionar una ciudad o coordenadas"}, status=400)

        response = requests.get(url)
        data = response.json()

        # Verificar si la respuesta es exitosa para obtener los datos del clima
        # y si no, devolver un mensaje de error adecuado
        if response.status_code == 200:
            weather_data = {
                "city": data.get("name"),
                "temperature": data["main"].get("temp"),
                "humidity": data["main"].get("humidity"),
                "description": data["weather"][0].get("description"),
                "icon": data["weather"][0].get("icon")
            }

            # Guardar en historial si el usuario está autenticado 
            if request.user.is_authenticated and weather_data["city"]:
                SearchHistory.objects.create(
                    user=request.user,
                    city=weather_data["city"],
                    temperature=data["main"].get("temp"),
                    humidity=data["main"].get("humidity"),
                    description=data["weather"][0].get("description")
                )

            return Response(weather_data)
        else:
            return Response({"error": data.get("message", "Error desconocido")}, status=response.status_code)

# Para saber el clima actualmente, pero con JsonResponse
def current_weather(request):
    city = request.GET.get('city')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    api_key = config("OPENWEATHER_API_KEY")

    if city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es"
    elif lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=es"
    else:
        return JsonResponse({"error": "Debe proporcionar una ciudad o coordenadas"}, status=400)

    response = requests.get(url)
    data = response.json()

    # Verificar si la respuesta es exitosa para obtener los datos del clima
    if response.status_code == 200:
        weather_data = {
            "city": data.get("name"),
            "temperature": data["main"].get("temp"),
            "humidity": data["main"].get("humidity"),
            "description": data["weather"][0].get("description"),
            "icon": data["weather"][0].get("icon")
        }
        return JsonResponse(weather_data)
    else:
        return JsonResponse({"error": data.get("message", "Error desconocido")}, status=response.status_code)


#Para saber el clima en los proximos dias 
class ForecastWeatherView(APIView):
    def get(self, request):
        city = request.GET.get('city')
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        API_KEY = config('OPENWEATHER_API_KEY')

        if city:
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
        else:
            url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'

        data = requests.get(url).json()
        return Response(data)

#Para buscar el clima de ciudades 
class CitySearchView(APIView):
    def get(self, request):
        query = request.GET.get('q')
        API_KEY = config('OPENWEATHER_API_KEY')


        if not query:
            return Response({"error": "Falta parámetro ?q="}, status=400)

        url = f'http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={API_KEY}'
        data = requests.get(url).json()
        return Response(data)

#Para saber si hay alertas meteorologicas
class WeatherAlertsView(APIView):
    def get(self, request):
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        API_KEY = config('OPENWEATHER_API_KEY')

        # Verifica que se hayan proporcionado las coordenadas
        # Si no se proporcionan, devuelve un error 400
        if not lat or not lon:
            return Response({"error": "Se requieren lat y lon"}, status=400)

        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily,current&appid={API_KEY}"
        data = requests.get(url).json()

        alerts = data.get("alerts", [])
        return Response({"alerts": alerts})

# Para ver el historial de busquedas de los usuarios, usa isOwnerOrReadOnly para que los usuarios solo puedan ver su propio historial
class SearchHistoryDetailView(generics.RetrieveUpdateDestroyAPIView): 
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Limita el acceso solo al historial del usuario autenticado
        return self.queryset.filter(user=self.request.user)

# Registro de usuarios
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente tras registrarse
            return redirect('home')  # Cambia esto a donde quieras redirigir
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Vista para el historial de búsqueda de los usuarios autenticados
@login_required
def weather_history_view(request):
    history = SearchHistory.objects.filter(user=request.user).order_by('-searched_at')
    return render(request, 'history.html', {'history': history})