from django.db import models

# Create your models here.

#Historial de busquedas de los usuarios
class SearchHistory(models.Model):
    city = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
