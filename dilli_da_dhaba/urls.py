from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customise built-in admin site labels from settings
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title  = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Public API
    path('api/', include('menu.api_urls')),

    # JWT auth tokens
    path('api/auth/', include('accounts.urls')),

    # Template-rendered pages
    path('', include('core.urls')),
    path('menu/', include('menu.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
