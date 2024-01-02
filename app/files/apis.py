from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from app.api.mixins import ApiAuthMixin
from app.files.models import File
from app.files.services import (
    FileDirectUploadService,
    FileStandardUploadService,
)


class FileListApi(APIView):
    def get(self, request):
        # Retrieve query parameters
        file_type = request.query_params.get('file_type')
        file_usage_type = request.query_params.get('file_usage_type')
        crm_document_type = request.query_params.get('crm_document_type')
        related_property = request.query_params.get('related_property')
        crm_lead = request.query_params.get('crm_lead')
        uploaded_by = request.query_params.get('uploaded_by')

        # Build query
        query = Q()
        if file_type:
            query &= Q(file_type=file_type)
        if file_usage_type:
            query &= Q(file_usage_type=file_usage_type)
        if crm_document_type:
            query &= Q(crm_document_type=crm_document_type)
        if related_property:
            query &= Q(related_property_id=int(related_property))
        if crm_lead:
            query &= Q(crm_lead_id=int(crm_lead))
        if uploaded_by:
            query &= Q(uploaded_by_id=int(uploaded_by))

        # Retrieve files
        files = File.objects.filter(query)

        # Create response data
        data = [{
            "id": file.id,
            "url": file.url,
            "name": file.original_file_name,
            # Include other relevant fields as needed
        } for file in files]

        return Response(data, status=status.HTTP_200_OK)


class FileRetrieveApi(APIView):
    def get(self, request, file_id):
        file = get_object_or_404(File, id=file_id)
        return Response({
            "id": file.id,
            "url": file.url,
            "name": file.original_file_name
        })


class FileStandardUploadApi(APIView):
    def post(self, request):
        data = request.data
        file_usage_type = data.get('file_usage_type', None)
        crm_document_type = data.get('crm_document_type', None)
        property = data.get('property', None)
        crm_lead = data.get('crm_lead', None)
        try:
            service = FileStandardUploadService(user=request.user,
                                                file_obj=request.FILES["file"],
                                                file_usage_type=file_usage_type,
                                                crm_document_type=crm_document_type,
                                                property=int(property) if property else None,
                                                crm_lead=crm_lead)
            file = service.create()
            res = {"id": file.id}
        except ValidationError as e:
            res = {
                'error_message': str(e),
                'error_code': e.args[0] if e.args else None,
            }

        return Response(data=res, status=status.HTTP_201_CREATED)


class FileDirectUploadStartApi(APIView):
    class InputSerializer(serializers.Serializer):
        file_name = serializers.CharField()
        file_type = serializers.CharField()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = FileDirectUploadService(request.user)
        presigned_data = service.start(**serializer.validated_data)

        return Response(data=presigned_data)


class FileDirectUploadLocalApi(APIView):
    def post(self, request, file_id):
        file = get_object_or_404(File, id=file_id)

        file_obj = request.FILES["file"]

        service = FileDirectUploadService(request.user)
        file = service.upload_local(file=file, file_obj=file_obj)

        return Response({"id": file.id})


class FileDirectUploadFinishApi(APIView):
    class InputSerializer(serializers.Serializer):
        file_id = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_id = serializer.validated_data["file_id"]

        file = get_object_or_404(File, id=file_id)

        service = FileDirectUploadService(request.user)
        service.finish(file=file)

        return Response({"id": file.id})

# class File(APIView):
#     class InputSerializer(serializers.Serializer):
#         file_id = serializers.CharField()
#
#     def post(self, request):
#         serializer = self.InputSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         file_id = serializer.validated_data["file_id"]
#
#         file = get_object_or_404(File, id=file_id)
#
#         service = FileDirectUploadService(request.user)
#         service.finish(file=file)
#
#         return Response({"id": file.id})
