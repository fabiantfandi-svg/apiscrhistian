import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

# Construir la ruta a la llave (ajusta el nombre de tu archivo .json)
base_path = Path(__file__).resolve().parent.parent
sdk_key_path = os.path.join(base_path, 'serviceAccountKey.json')

# Inicializar Firebase
cred = credentials.Certificate(sdk_key_path)
firebase_admin.initialize_app(cred)

# Esta es la función que te falta o que tiene el nombre mal escrito:
def get_firestore_client():
    return firestore.client()