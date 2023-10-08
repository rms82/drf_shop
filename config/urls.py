from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



from .shemas import schema_view

urlpatterns = [
    #  DEBUG TOOLBAR
    path("__debug__/", include("debug_toolbar.urls")),

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

    # APSS 
    path("shop/", include("shop.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
