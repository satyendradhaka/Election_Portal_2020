from django.urls import path, include
from . import views 
urlpatterns = [
	path('', views.home),
	path('geo/', views.save_user_geolocation),
]


##home page: login with outlook wala
## home page : if logged in ask for camera and location permission
##verification: geolocation and image capturing
##captcha should be on verification page with image and geolocation
##voter: voter details
##voter/vote: voting page name and there roll number year can be determined and department( better ask contenstants for about in fixed lines)
##voter/review page: all the contenstants who has voted
##voter/done: process completed thank, review page, thank u page and credits page