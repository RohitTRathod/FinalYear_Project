from django.urls import path
from .views import predict_churn

urlpatterns = [
    path('', predict_churn, name='predict_churn'),
]