from django.urls import path, include
from . import views


urlpatterns = [
    path('verify/',views.verify,name="captcha"),
    path('vote/',views.vote,name="vote"),
]
