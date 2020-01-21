from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

international_urls = i18n_patterns(
    path('admin/', admin.site.urls),
)

rest_url = [path('api/', include('cidade_ajuda.rest.urls')), path('api-auth/', include('rest_framework.urls')), ]

#static_urls = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
#              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = international_urls + rest_url
