from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission pour n'autoriser que les admins à modifier un objet
    """
    def has_permission(self, request, view):
        # Tout le monde peut "lire" l'objet
        # SAFE_METHODS =  GET, HEAD ou OPTIONS => autorisé
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permission en écriture seulement si admin
        return request.user and request.user.is_staff
