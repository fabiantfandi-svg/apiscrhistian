from django.urls import path
from .views import TareaAPIView

urlpatterns=[
    path('tareas/', TareaAPIView.as_view(), name="api_tareas"),
    path('tareas/<str:tarea_id>/', TareaAPIView.as_view(), name="api_tarea_detalle"),
]