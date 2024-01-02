from django.contrib.auth import get_user_model
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
