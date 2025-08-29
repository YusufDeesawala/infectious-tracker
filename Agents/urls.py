from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/top-diseases', views.top_diseases, name='top_diseases'),
    path('api/top-outbreaks', views.top_outbreaks, name='top_outbreaks'),
    path('api/top-meds', views.top_meds, name='top_meds'),
]