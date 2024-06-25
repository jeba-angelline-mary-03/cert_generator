from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('certificates/', include('certificates.urls')),
    path('', include('certificates.urls')),  # Handle the root URL
    path('accounts/', include('django.contrib.auth.urls')),  # Include built-in auth URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)