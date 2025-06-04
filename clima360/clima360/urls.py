"""
URL configuration for clima360 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from weather.views import ForecastWeatherView, CurrentWeatherView, CitySearchView, WeatherAlertsView, home, weather_history_view, register
from weather.swagger import urlpatterns as swagger_urls
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', home, name='home'),
    path('api/weather/current', CurrentWeatherView.as_view()),
    path('api/weather/forecast', ForecastWeatherView.as_view()),
    path('api/cities/search', CitySearchView.as_view()),
    path('api/weather/alerts', WeatherAlertsView.as_view()),
    path('historial/', weather_history_view, name='weather-history'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


]

urlpatterns += swagger_urls
