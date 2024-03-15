from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from app.users.models import User, Customer


class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'mobile_no', 'role', 'director')


class UserAdminChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'mobile_no', 'role', 'director', 'password')


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ('id', 'name', 'username', 'email', 'mobile_no', 'role', 'created_at', 'updated_at', 'director')
    search_fields = ('name', 'username', 'email', 'mobile_no')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('name', 'email', 'mobile_no', 'role', 'director')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'email', 'mobile_no', 'role', 'director', 'password1', 'password2'),
        }),
    )


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile_no', 'email', 'occupation', 'created_at', 'updated_at')
    search_fields = ('name', 'mobile_no', 'email')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
