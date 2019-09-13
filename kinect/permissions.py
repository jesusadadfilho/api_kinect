from rest_framework import permissions

#Abaixo é apenas um teste, preparando caso haja um sistema de permissões
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.owner == request.user
