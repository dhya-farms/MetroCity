from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from app.users.models import User, Customer, FAQ, UserQuery


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'address', 'mobile_no', 'role', 'points', 'director')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('last_login', 'date_joined', 'created_at', 'updated_at')  # Add automatic fields here
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal info', {'fields': ('name', 'email', 'mobile_no', 'role', 'points', 'director')}),
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


class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_preview', 'is_faq', 'created_at', 'updated_at')
    list_filter = ('is_faq', 'created_at', 'updated_at')
    search_fields = ('question', 'answer')
    list_editable = ('is_faq',)
    fields = ('question', 'answer', 'is_faq', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    def question_preview(self, obj):
        """Create a short preview of the question for the list display."""
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question

    question_preview.short_description = "Question Preview"


class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('short_question', 'is_resolved', 'created_at', 'updated_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('question', 'response')
    readonly_fields = ('created_at', 'updated_at')

    def short_question(self, obj):
        """Create a short preview of the question for the list display."""
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    short_question.short_description = "Question"


admin.site.register(UserQuery, UserQueryAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Customer, CustomerAdmin)
