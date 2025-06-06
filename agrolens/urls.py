from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexlens, name='indexlens')
]
