from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path

# Swagger configuration para Clima360 API documentation, sirve para generar la documentación interactiva de la API usando drf-yasg
schema_view = get_schema_view(
    openapi.Info(
        title="Clima360 API",
        default_version='v1',
        description="Documentación de la API Clima360",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
