from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError

from app.utils.controllers import Controller
from app.utils.helpers import get_serialized_exception
from app.users.models import User, Customer

UserModel = get_user_model()


class UserController(Controller):
    def __init__(self):
        self.model = UserModel


class CustomerController(Controller):
    def __init__(self):
        self.model = Customer

    def create(self, **kwargs):
        try:
            instance = self.model.objects.create(**kwargs)
            return None, instance
        except (IntegrityError, ValueError) as e:
            return get_serialized_exception(e)

    def edit(self, instance_id, **kwargs):
        try:
            instance = self.model.objects.get(id=instance_id)
            for attr, value in kwargs.items():
                if attr == 'image' and isinstance(value, InMemoryUploadedFile):
                    # Handle image file separately if it's part of the update
                    getattr(instance, attr).save(value.name, value, save=True)
                elif value is not None:
                    setattr(instance, attr, value)
            instance.save()
            return None, instance
        except (IntegrityError, ValueError) as e:
            return get_serialized_exception(e)
