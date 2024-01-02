from typing import Optional

from django.db import transaction

from app.common.services import model_update
from app.users.models import User


def user_create(
    *, email: str, is_active: bool = True, is_admin: bool = False, password: Optional[str] = None
) -> User:
    user = User.objects.create_user(email=email, is_active=is_active, is_admin=is_admin, password=password)

    return user


@transaction.atomic
def user_update(*, user: User, data) -> User:
    non_side_effect_fields = ["first_name", "last_name"]

    user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user
