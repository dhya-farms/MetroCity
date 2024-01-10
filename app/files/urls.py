from django.urls import include, path

from app.files.apis import (
    FileDirectUploadFinishApi,
    FileDirectUploadLocalApi,
    FileDirectUploadStartApi,
    FileStandardUploadApi, FileRetrieveApi, FileListApi,
)

urlpatterns = [
    path('files/', FileListApi.as_view(), name='file-list'),
    path('file/<int:file_id>/', FileRetrieveApi.as_view(), name='file-retrieve'),
    path(
        "upload/",
        include(
            [
                path("standard/", FileStandardUploadApi.as_view(), name="standard"),
                path(
                    "direct/",
                    include(
                        [
                            path("start/", FileDirectUploadStartApi.as_view(), name="start"),
                            path("finish/", FileDirectUploadFinishApi.as_view(), name="finish"),
                            path("local/<str:file_id>/", FileDirectUploadLocalApi.as_view(), name="local"),
                        ]
                    ),
                ),
            ],
        ),
    ),
]
