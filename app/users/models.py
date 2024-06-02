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
        default=generate_random_username,
        unique=True
    )
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True, blank=True, null=True)
    mobile_no = models.CharField(
        max_length=10, unique=True, validators=[
            RegexValidator(regex=r'^\d{10}$', message="Provide Proper 10 digit Phone Number")
        ],
        db_index=True, blank=True, null=True
    )
    role = models.IntegerField(choices=Role.choices, blank=True, null=True)
    points = models.IntegerField(default=0)
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


class FAQ(models.Model):
    question = models.TextField(help_text="Frequently asked question.")
    answer = models.TextField(help_text="Answer to the question.", blank=True, null=True)
    is_faq = models.BooleanField(default=False, help_text="Designates whether the entry is an approved FAQ.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question[:50]} - {'FAQ' if self.is_faq else 'Question'}"


class UserQuery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_queries',
                             help_text="The user who raised this query.", blank=True, null=True)
    question = models.TextField(help_text="User-submitted query.")
    response = models.TextField(blank=True, null=True, help_text="Admin response to the query.")
    is_resolved = models.BooleanField(default=False, help_text="Whether the query has been resolved.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question[:50]} - {'Resolved' if self.is_resolved else 'Pending'}"


class Customer(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, blank=True, null=True)
    favorites = models.ManyToManyField('properties.Phase', related_name='favorited_by', blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='customers/profile_images/', blank=True, null=True)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField('email address', blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    preferences = JSONField(blank=True, null=True)
    # {"area_of_purpose": [1, 2], "property_types": [1, 3]}
    address = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='created_customers',
                                   blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"id: {self.id}. {self.name} [{self.mobile_no}]"
