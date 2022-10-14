from rest_framework.permissions import AllowAny


class NonAuthPostOnly(AllowAny):
    def has_permission(self, request, view):
        if request.method == 'POST' and not request.user.is_authenticated:
            return True
        return False
