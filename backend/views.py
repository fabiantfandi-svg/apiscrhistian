from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TareasSerializer
from api_tareas.firebase_config import get_firestore_client
from firebase_admin import firestore

db = get_firestore_client()

class TareaAPIView(APIView):
    """
    Endpoint para listar todas las tareas (GET) y crear una nueva tarea (POST)
    """
    def get(self, request):
        try:
            #Traer todos los datos de la coleccion de firestore
            docs = db.collection('api_tareas').stream()
            tareas = []
            for doc in docs:
                tarea_data = doc.to_dict()
                tarea_data['id']=doc.id
                tareas.append(tarea_data)
            return Response({"mensaje": "Exito", "datos": tareas}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post (self, request):
        #1. Pasar el JSON al serializer para que valide los campos
        serializer = TareasSerializer(data=request.data)

        #2. si el json cumple las reglas
        if serializer.is_valid():
            datos_validados = serializer.validated_data

            datos_validados['fecha_creacion'] = firestore.SERVER_TIMESTAMP

            try:
                #3. Guardamos las datos en firestore
                nuevo_doc = db.collection('api_tareas').add(datos_validados)
                #obtener el id generado
                id_generado = nuevo_doc[1].id

                return Response({
                    "mensaje":"Tarea creada correctamente",
                    "id":id_generado
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"Error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)