from django.db import models
from django.contrib.auth.models import User


# Create your models here.

#Historial de busquedas de los usuarios
class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    temperature = models.FloatField()
    humidity = models.IntegerField()
    description = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)

    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.city or f'{self.latitude},{self.longitude}'} at {self.searched_at.strftime('%Y-%m-%d %H:%M:%S')}"
