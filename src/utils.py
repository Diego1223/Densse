import mysql.connector
from mysql.connector import Error
import shutil

CONFIG = {
    "host":"localhost",
    "user": "root",
    "password": "tuclave",
    "database":"checklist",
    "auth_plugin":"mysql_native_password"
}

PALABRAS_PROHIBIDAS = [
    "tonto", "pendejo", "estupido", "mierda", "caca", "popo",
    "culero", "zorra", "carajo", "verga"   
]

def centrar_texto(texto):
    ancho_terminal = shutil.get_terminal_size().columns
    texto_centrado = texto.center(ancho_terminal)
    print(texto_centrado)


class Database:
    def __init__(self, config: dict):
        self.config = config
        self.conexion = None
        self.cursor = None
    
    def conectar(self):
        try:
            self.conexion = mysql.connector.connect(**self.config)
            self.cursor = self.conexion.cursor()
            return self
        except Error as e:
            print(f"Error al conectarse Mysql: {e}")
            return None
    def cerrar(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conexion:
                self.conexion.close()
        except Error as e:
            print(f"Error al conectarse a Mysql: {e}")

    def ejecutar(self, query, params=None, commit=False):
        try:
            #En dado caso que no pasemos parametros se guardara = ()
            self.cursor.execute(query, params or ())
            if commit:
                self.conexion.commit()
            return self.cursor
        except Error as e:
            print(f"Error al consultar {e}")
            return None