from django.contrib import admin
from django.urls import path, include

from .shemas import schema_view

urlpatterns = [
    # DJANGO 
    path("admin/", admin.site.urls),

    # API UI
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),


]
