from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('subscriptions/', include('apps.subscriptions.urls')),
    path('payments/', include('apps.payments.urls')),
    path('channels/', include('apps.channels.urls')),
    path('broadcasts/', include('apps.broadcasts.urls')),
    path('support/', include('apps.support.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('api/', include('apps.api.urls')),
    path('bot/', include('apps.bot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
