from django import forms
from django.contrib import admin
from django.utils import timezone

from .models import File, User
from .utils import file_generate_name


class FileForm(forms.ModelForm):
    original_file_name = forms.CharField(disabled=True, required=False)
    file_type = forms.CharField(disabled=True, required=False)
    file_name = forms.CharField(disabled=True, required=False)
    uploaded_by = forms.ModelChoiceField(queryset=User.objects.all(), disabled=True, required=False)
    file = forms.FileField()

    class Meta:
        model = File
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            if 'original_file_name' in self.fields:
                self.fields['original_file_name'].initial = getattr(self.instance, 'original_file_name', None)
            if 'file_type' in self.fields:
                self.fields['file_type'].initial = getattr(self.instance, 'file_type', None)
            if 'file_name' in self.fields:
                self.fields['file_name'].initial = getattr(self.instance, 'file_name', None)
            if 'uploaded_by' in self.fields:
                self.fields['uploaded_by'].initial = getattr(self.instance, 'uploaded_by', None)

    def clean(self):
        cleaned_data = super().clean()
        file = self.files.get('file')  # Access the uploaded file directly
        if file:
            cleaned_data['file_name'] = file_generate_name(file.name)
            cleaned_data['file_type'] = file.content_type
            cleaned_data['original_file_name'] = file.name
        return cleaned_data


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_file_name', 'file_name', 'file_type', 'file_usage_type', 'crm_document_type',
                    'uploaded_by', 'upload_finished_at', 'created_at', 'updated_at')
    list_filter = ('file_type', 'file_usage_type', 'crm_document_type', 'uploaded_by')
    search_fields = ('original_file_name', 'file_name')
    readonly_fields = (
        'upload_finished_at', 'file_name', 'original_file_name', 'file_type', 'uploaded_by', 'created_at', 'updated_at')
    date_hierarchy = 'upload_finished_at'
    form = FileForm

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not obj:  # If creating a new object
            for field in ['file_name', 'original_file_name', 'file_type', 'uploaded_by', 'upload_finished_at',
                          'created_at', 'updated_at']:
                if field in fields:
                    fields.remove(field)
        return fields

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by_id:
            obj.uploaded_by = request.user

        if 'file' in request.FILES:
            file = request.FILES['file']
            obj.file_name = file_generate_name(file.name)
            obj.original_file_name = file.name
            obj.file_type = file.content_type

        if not obj.upload_finished_at:
            obj.upload_finished_at = timezone.now()

        super().save_model(request, obj, form, change)
