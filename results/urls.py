from django.urls import path
from . import views

urlpatterns = [
	path('results/public',views.publicKey,name="publicKey"),
	path('results/private',views.privateKey,name="privateKey"),
	path('results/keyUpload',views.keyUpload,name="keyUpload"),
	path('results/view/<str:post>/',views.results_view,name="results_view"),
	path('results/',views.results,name="results"),

	
]