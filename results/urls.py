from django.urls import path
from . import views

urlpatterns = [
	path('results/public',views.publicKey,name="publicKey"),
	path('results/',views.results,name="results"),
	
]