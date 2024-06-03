from django.core.exceptions import PermissionDenied


class UserRequiredMixin:
    """Класс для проверки авторизации пользователя"""

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise PermissionDenied
        return self.object
