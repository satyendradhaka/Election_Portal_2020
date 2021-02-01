from django.urls import path
from . import views

urlpatterns = [
    path('stats/',views.pollStats,name="pollStats"),
    path('ugDeptStats/',views.ugDeptStats,name="ugDeptStats"),
]