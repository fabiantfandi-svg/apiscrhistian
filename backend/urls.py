from django.urls import path
from .views import TareaAPIView

urlpatterns=[
    path('tareas/', TareaAPIView.as_view(), name="api_tareas")
]