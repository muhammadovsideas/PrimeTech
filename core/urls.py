from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.i18n import i18n_patterns

schema_view = get_schema_view(
   openapi.Info(
      title="Prime-Tech",
      default_version='v1',
      description="e-commerce website",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 🔹 bu majburiy: Django built-in language URLs
    path("i18n/", include("django.conf.urls.i18n")),
    # 🔹 Admin
    path("admin/", admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', include('main.urls')),
    path("docs/", schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger-ui"),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

