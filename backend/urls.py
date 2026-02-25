from django.urls import path
from .views import TareasAPIView
from .views_auth import RegistroAPIView, LoginApiView

urlpatterns=[
    path('auth/registro/', RegistroAPIView.as_view(), name="api_registro"),
    path('auth/login/', LoginApiView.as_view(), name="api_login"),


    path('tareas/', TareasAPIView.as_view(), name="api_tareas"),
    path('tareas/<str:tarea_id>/', TareasAPIView.as_view(), name="api_tarea_detalle"),
]