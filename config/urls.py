from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('posts.api_urls')),
    path('posts/', include('posts.urls')),
    path('polls/', include('polls.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
