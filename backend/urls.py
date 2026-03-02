from django.urls import path
from .views import TareasAPIView
from .views_auth import RegistroAPIView, LoginApiView
from .views_perfil import PerfilImagenAPIView

urlpatterns=[
    path('auth/registro/', RegistroAPIView.as_view(), name="api_registro"),
    path('auth/login/', LoginApiView.as_view(), name="api_login"),


    path('tareas/', TareasAPIView.as_view(), name="api_tareas"),
    path('tareas/<str:tarea_id>/', TareasAPIView.as_view(), name="api_tarea_detalle"),

    path('perfil/foto/', PerfilImagenAPIView.as_view(), name="api_perfil_foto"),

]