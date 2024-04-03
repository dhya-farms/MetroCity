from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db.models import JSONField
from django.urls import reverse
from django.db import models
from app.users.enums import Role
from django.utils.translation import gettext_lazy as _

from app.utils.helpers import generate_random_username


class User(AbstractUser):

    username_validator = UnicodeUsernameValidator()

    name = models.CharField(max_length=255)
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        default=generate_random_username(),
        unique=True
    )
    email = models.EmailField(_('email address'), unique=True, blank=True, null=True)
    mobile_no = models.CharField(max_length=10, unique=True, validators=[
        RegexValidator(regex=r'^\d{10}$', message="Provide Proper 10 digit Phone Number")],
                                 db_index=True, blank=True, null=True)
    role = models.IntegerField(choices=Role.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    director = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="sales_officers")

    def __str__(self):
        return f"id: {self.id}. {self.name} [{self.mobile_no}]"

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"mobile_no": self.mobile_no})


class Customer(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='customers/profile_images/', blank=True, null=True)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField('email address', blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    preferences = JSONField(blank=True, null=True)
    # {"area_of_purpose": [1, 2], "property_types": [1, 3]}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
