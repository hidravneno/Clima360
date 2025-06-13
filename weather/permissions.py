from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permite que solo el dueño de un objeto lo edite o elimine.
    Los demás solo pueden leerlo.
    """

    def has_object_permission(self, request, view, obj):
        # Lectura permitida para cualquier solicitud
        if request.method in permissions.SAFE_METHODS:
            return True
        # Escritura permitida solo al dueño del objeto
        return obj.user == request.user
