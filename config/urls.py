import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('user.urls')),
    path('', include('appointment.urls')),
    path('comments/', include('comments.urls')),

]

if settings.DEBUG:
    urlpatterns += path('debug/', include(debug_toolbar.urls)),
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
