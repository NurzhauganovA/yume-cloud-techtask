from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import settings


API_VERSION = 'v1'
API_URL = f'api/{API_VERSION}'

schema_view = get_schema_view(
    openapi.Info(
        title="Order Product Catalog API",
        default_version=API_VERSION,
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    path(f'{API_URL}/auth/', include('auth_user.urls')),
    path(f'{API_URL}/core/', include('core.urls')),

    path(f'{API_URL}/swagger/ui', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
