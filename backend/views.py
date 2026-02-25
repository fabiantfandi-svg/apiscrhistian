from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TareasSerializer
from api_tareas.firebase_config import initialize_firebase
from firebase_admin import firestore
from rest_framework.permissions import IsAuthenticated
from .authentication import FirebaseAuthentication

db = initialize_firebase()

class TareasAPIView(APIView):

    # Traemos nuestra autenticacion
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    """
    Endpoint para listar todas las tareas (GET) y crear una nueva tarea (POST)
    """
    def get(self, request, tarea_id=None):
        # GET ahora solo trae las tareas del usuario del dueño del token

        uid_usuario = request.user.uid
        try:
            #Traer todos los datos de la seleccion de firestore
            docs = db.collection('api_tareas').where('usuario_id', "==", uid_usuario).stream()
            tareas = []
            for doc in docs:
                tarea_data = doc.to_dict()
                tarea_data['id'] = doc.id
                tareas.append(tarea_data)
            
            return Response({"mensaje": "Exito", "Datos": tareas}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        #1. Pasar el JSON al serializador para que valide los campos

        serializer = TareasSerializer(data=request.data)

        # 2. Si el json cumple las reglas 
        if serializer.is_valid():
            datos_validados = serializer.validated_data

            datos_validados['usuario_id'] = request.user.uid
            datos_validados['fecha_creacion'] = firestore.SERVER_TIMESTAMP

            try:
                #3. Guardamaos los datos en firestore
                nuevo_doc = db.collection('api_tareas').add(datos_validados) 
                # Obtener el id generado
                id_generado = nuevo_doc[1].id
                return Response({"mensaje": "La tarea fue creada correctamente", "id": id_generado}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        # 1. Pasar el json por el serializador

        doc_ref = db.collection('api_tareas').document(pk)
        doc = doc_ref.get()
        try: 
            if not doc.exists:
                return Response({"Error": "La tarea no existe"}, status=status.HTTP_404_NOT_FOUND)
            
            tarea_data = doc.to_dict()

            if tarea_data.get('usuario_id') != request.user.id:
                return Response({"error": "No tienes permiso para editar esta tarea"}, status=status.HTTP_403_FORBIDDEN)
            serializer = TareasSerializer(data=request.data)
            if serializer.is_valid():
                doc_ref.update(serializer.validated_data)

                return Response({
                    "mensaje": f"La tarea {pk} fue actualizada correctamente",
                    "id": pk,
                    "datos": serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, pk):
        """
        Delete : eliminar una tarea especifica por id. El id viene de la url
        """

        if not pk:
            return Response({"Error": "Se requierte el id de alguna tarea"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            #Referencia al documento
            tarea_ref = db.collection('api_tareas').document(pk)
            doc = tarea_ref.get()

            #Verificar que el doc existe antes de borrarlo
            if not doc.exists:
                return Response({"Error": "No se encontro el archivo"}, status=status.HTTP_404_NOT_FOUND)
            tarea_ref.delete()

            tarea_data = doc.to_dict()

            if tarea_data.get('usuario_id') != request.user.id:
                return Response({"error": "No tienes permiso para editar esta tarea"}, status=status.HTTP_403_FORBIDDEN)

            return Response({"mensaje": f"Tarea {pk} se ha eliminado correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)