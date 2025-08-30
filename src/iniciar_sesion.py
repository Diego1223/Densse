import os 
import getpass
from utils import Database, centrar_texto
import json
import os


SESSION_FILE = "session.json"

class Sesion:
    def __init__(self):
        self.usuario = None
        self.user_id = None
        self._nombre = None
    
    def guardar_sesion(self,user_id, nombre):
        self.user_id = user_id
        self._nombre = nombre
        self.usuario = {"user_id": user_id, "nombre": nombre}
        with open(SESSION_FILE, "w") as f:
            json.dump(self.usuario,f)
    
    def cargar_sesion(self):
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
                self.user_id = data.get("user_id")
                self._nombre = data.get("nombre")
                self.usuario = data
                return self
        return None   

    def borrar_sesion(self):
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        self.usuario = None
        self.user_id = None
        self.nombre = None

    @property 
    def nombre(self):
        return self._nombre
        
class Iniciar_sesion:
    def __init__(self, db: Database):
        self.db = db
        self.usuario = None
        self.user_id = None
        self.nombre = None

    def login(self):
        os.system("clear")
        centrar_texto("=== Iniciar Sesion ===")
        email = input("Email -> ")
        contrasena = getpass.getpass("Contrasena -> ")

        sql = "SELECT id, nombre FROM usuarios WHERE correo = %s AND contrasena = %s"
        params = (email, contrasena)

        cursor = self.db.conectar()
        cursor = self.db.ejecutar(sql, params)

        if cursor:
            usuario = cursor.fetchone() #Fetchone regresa una tupla
            if usuario:
                self.user_id, self.nombre = usuario
                print(f"Bienvenido {self.nombre}")
                print(f"Encontrado como el usuario {usuario[0]}")
                self.usuario = usuario
                Sesion.guardar_sesion(self.usuario[0], self.usuario[1])
                return True
            else:
                print("Email o contrasena incorrectos")
                return False
        else:
            print("Error al ejecutar la consulta")
            return False      
            