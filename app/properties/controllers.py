from django.db import IntegrityError

from app.utils.controllers import Controller
from app.utils.helpers import get_serialized_exception
from app.properties.models import Property, Plot, Phase, Update


class UpdateController(Controller):
    def __init__(self):
        self.model = Update

    def filter(self, **filters):
        instance_qs = self.model.objects.all().order_by('-posted_by')
        return None, instance_qs


class PropertyController(Controller):
    def __init__(self):
        self.model = Property


class PhaseController(Controller):
    def __init__(self):
        self.model = Phase


class PlotController(Controller):
    def __init__(self):
        self.model = Plot
