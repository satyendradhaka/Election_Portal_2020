from django.urls import path, include
from . import views 
urlpatterns = [
	path('geo/', views.save_user_geolocation),
]
