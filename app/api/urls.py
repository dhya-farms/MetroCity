from django.urls import include, path

urlpatterns = [
    path("auth/", include(("app.authentication.urls", "authentication"))),
    path("users/", include(("app.users.urls", "users"))),
    path("errors/", include(("app.errors.urls", "errors"))),
    path("files/", include(("app.files.urls", "files"))),
]
