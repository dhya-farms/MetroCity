import django_filters

from app.users.models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ("id", "email")
