from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('', include('geolocation.urls')),
	path('voter/', include('voter.urls')),
	path('admin/', admin.site.urls),
    path('oauth2/', include('django_auth_adfs.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
# 	urlpatterns+=static(settings.STATIC_URL)
