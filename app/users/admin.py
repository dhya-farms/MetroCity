from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app.users.models import User, Customer
from django.utils.translation import ugettext_lazy as _


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('name', 'email', 'mobile_no', 'role', 'director')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined', 'created_at', 'updated_at')  # Add automatic fields here
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        (_('Personal info'), {'fields': ('name', 'email', 'mobile_no', 'role', 'director')}),
    )
    list_display = ('id', 'username', 'email', 'name', 'mobile_no', 'is_staff', 'created_at')
    search_fields = ('username', 'name', 'email', 'mobile_no')
    ordering = ('username',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('created_at', 'updated_at')
        return self.readonly_fields


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile_no', 'email', 'occupation', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'mobile_no', 'email')
    # raw_id_fields = ('user',)  # Use raw_id_fields for ForeignKey or OneToOneField relations for better performance
    readonly_fields = ('created_at', 'updated_at')  # Mark automatic timestamps as read-only

    fieldsets = (
        (None, {'fields': ('user', 'name', 'mobile_no', 'email', 'occupation', 'image', 'address')}),
        ('Preferences', {'fields': ('preferences',)}),
        ('Relations', {'fields': ('favorites', 'created_by')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    filter_horizontal = ('favorites',)  # Efficient many-to-many editing

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('created_at', 'updated_at')
        return self.readonly_fields


admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
