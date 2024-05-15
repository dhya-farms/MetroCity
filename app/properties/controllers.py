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

    def filter(self, **filters):
        properties_queryset = self.model.objects.filter(
            phases__plots__is_sold=False
        ).distinct()
        for attr, value in filters.items():
            if value is not None:
                properties_queryset = properties_queryset.filter(**{attr: value})
        return None, properties_queryset


class PhaseController(Controller):
    def __init__(self):
        self.model = Phase

    def filter(self, **filters):
        phases_queryset = self.model.objects.filter(
            plots__is_sold=False
        ).distinct()
        for attr, value in filters.items():
            if value is not None:
                phases_queryset = phases_queryset.filter(**{attr: value})
        return None, phases_queryset


class PlotController(Controller):
    def __init__(self):
        self.model = Plot

    def filter(self, **filters):
        plots_queryset = self.model.objects.filter(
            is_sold=False
        ).distinct()
        for attr, value in filters.items():
            if value is not None:
                plots_queryset = plots_queryset.filter(**{attr: value})
        return None, plots_queryset
