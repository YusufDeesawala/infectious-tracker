from django.urls import path
from . import views

urlpatterns = [
    path('api/top-diseases', views.top_diseases, name='top_diseases'),
    path('api/top-outbreaks', views.top_outbreaks, name='top_outbreaks'),

]