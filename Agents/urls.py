from django.urls import path
from . import views

urlpatterns = [
    path('api/top-diseases', views.top_diseases, name='top_diseases'),
    path('api/top-news', views.top_news, name='top_news'),

]