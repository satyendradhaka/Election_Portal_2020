from django.urls import path
from . import views

urlpatterns = [
    path('stats/',views.pollPercent,name="pollPercent"),
    path('statsugpg/',views.UgPgStats,name="UgPg"),
]