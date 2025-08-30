import os
import getpass
from utils import Database, centrar_texto, PALABRAS_PROHIBIDAS, CONFIG
from iniciar_sesion import Iniciar_sesion, Sesion
from tareas import Tareas
import re


class Tablas:
    def __init__(self, db: Database):
        self.db = db

    def crear_tablas(self):
        query_usuarios = """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(100) NOT NULL UNIQUE,
                contrasena VARCHAR(100) NOT NULL,
                edad SMALLINT NOT NULL
            );
        """
        #ON DELETE ON CASCADE -> quiere decir que si un registro de la tabla padre se borra o modifica lo hara tambien en la
        #tabla hija
        #En realidad esta tabla quedaria asi despues de algunas modificaciones:
        """
            DROP TABLE IF EXISTS tareas;

            CREATE TABLE tareas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT NOT NULL,
            hora TIME,
            tarea VARCHAR(500),
            prioridad SMALLINT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            );
        """
        query_tareas = """
            CREATE TABLE IF NOT EXISTS tareas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT NOT NULL,
                hora TIME,
                tarea VARCHAR(500),
                prioridad SMALLINT(3),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            );
        """

        self.db.ejecutar(query_usuarios, commit=True)
        self.db.ejecutar(query_tareas, commit=True)

class Registrarse:
    def __init__(self, db:Database):
        self.db = db

    
    def detector(self,nombre_usuario: str) -> bool:
        usuario = nombre_usuario.lower()

        for palabra in PALABRAS_PROHIBIDAS:
            if palabra in usuario:
                return True
        return False

    def validar_contrasena(self,contrasena: str) -> bool:
        errores = []

        if len(contrasena) < 8 or len(contrasena) > 15:
            errores.append("La contrasena debe tener entre 8 y 15 caracteres")
        if not any(c.isupper() for c in contrasena):
            errores.append("La contrasena debe contener al menos una letra mayuscula")
        if not any(c.islower() for c in contrasena):
            errores.append("La contrasena debe contener al menos una letra minuscula")
        if not any(c.isdigit() for c in contrasena):
            errores.append("La contrasena debe contener al menos un numero")
        if not any(c in "!@#$%^&*()-_+" for c in contrasena):
            errores.append("La contrasena debe contener caracteres especiales")
        
        if len(errores) == 0:
            print("Contrasena segura")
            return True
        else:
            print("Se encontraron algunos errores en tu contrasena")
            for e in range(len(errores)):
                print(f"{e + 1}. {errores[e]}") 
            return False
    #ESTA FUNCION VALIDA QUE EL CORREO contenga "@" y ademas tenga un @gmail, @hotmail, etc
    def validar_correo(self, correo: str) -> bool:
        dominios = [
            "gmail", "icloud", "hotmail", "outlook"
        ]
        correo_validar = correo.lower()
        #Lo convertimos en un patron que entiende regex es como decirle
        #Busca gmail.com o hotmail.com o outlook.com en el texto
        patron = "(" + "|".join(dominios) + ")"

        if not any(c in "@" for c in correo_validar):
            print("Correo incorrecto")
            return False
        else:
            if re.search(patron, correo):
                print("Correo valido")
            else:
                print("Invalido")
                return False
            return True


    def agregar_usuario(self):
        os.system("clear")
        centrar_texto("=== REGISTRO DE USUARIO ===")   

        # ========== PEDIR NOMBRE ==========
        #Primero se pide el nombre y se valida que no tenga ninguna palabra ofensiva
        intentos = 1
        while intentos <= 3:
            nombre = input("Nombre => ").strip() #Elimina los caracteres espaciados al principio y al final
            if self.detector(nombre):
                print("Tu nombre es ofensivo. Vuelve a intentarlo\n")
            else:
                print("Nombre valido\n")
                break
            
            if intentos >= 3:
                print("Saliendo...")
                exit() #Sale del programa 
            intentos += 1   

        # ================= VALIDAR CORREO ELECTRONICO =================           
        correo = input("Correo (solo gmail, hotmail y icloud) => ").strip()
        intentos = 1
        while self.validar_correo(correo) != True:
            print("Tu correo esta incorrecto. Vuelve a intentarlo\n")
            correo = input("=> ")

            if intentos >= 3:
                print("Saliendo...`")
                exit()

        
        # ===== VALIDAR CONTRASENA ===== 
        intentos = 1
        while intentos <= 3:
            contrasena = getpass.getpass("Ingresa una contrasena segura => ").strip()              
            
            if self.validar_contrasena(contrasena):
                break 
            else:
                print("\n")
            
            if intentos == 3:
                print("Saliendo...")
            intentos += 1  

        try:
            edad = int(input('Registra tu edad =>'))
        except:
            print("Error")

        #Guardar y mandar todos los datos a la base de datos
        query_usuario = "INSERT INTO usuarios (nombre, correo, contrasena, edad) VALUES(%s,%s, %s, %s);"
        parametros = (nombre, correo, contrasena, edad)
        self.db.conectar()
        self.db.ejecutar(query_usuario, parametros, commit=True)
        self.db.cerrar() 


# ----- MAIN PROGRAM ------ 
if __name__ == '__main__':
    try:
        db = Database(CONFIG).conectar()
        if db:
            tablas = Tablas(db)
            tablas.crear_tablas()
            db.cerrar()
        
        texto_centrado = "Bienvenido"

        usuario = Sesion()
        usuario = usuario.cargar_sesion()

        if usuario:
            centrar_texto(f"Bienvenido {usuario.nombre}")
            print("\n")        
            tareas = Tareas(db, usuario.user_id) 
            while True:
                centrar_texto("1.Agregar 2. Ver tareas 3.Eliminar")
                op = int(input("=> "))
                
                if op == 1:
                    centrar_texto("\nEscribe la tarea que deseas agregar, con una hora y la prioridad del 1 al 3\n")
                    tarea = input("Escribe la tarea => ")
                    hora = input("Escribe una hora para realizarlo => ")
                    prioridad = int(input("Escribe el nivel de prioridad => "))

                    tareas.agregar_tarea(tarea, hora, prioridad)
                if op == 2:
                    tareas.ver_tareas()
                
                if op == 3:
                    centrar_texto("Estas son las tareas que tienes, cual deseas eliminar?\n")
                    tareas.ver_tareas()
                    eliminar = int(input("=> "))
                    tareas.eliminar_tareas(eliminar)
                    

        else:        
            centrar_texto(texto_centrado)
            print("\n")
            opciones = "1.Registrarse\t2.Iniciar sesion" 
            centrar_texto(opciones)

            intentos = 1
            while intentos <= 3:
                try: 
                    op = int(input("=> "))
                    if op == 1:
                        registrarse = Registrarse(db)
                        registrarse.agregar_usuario() 
                        break
                    if op == 2:
                        login = Iniciar_sesion(db)
                        if login.login():
                            print("Sesion iniciada correctamente")
                        else:
                            print("No se puede iniciar sesion")
                            

                except ValueError:
                    print("Error!!!\nVuelve a intentarlo...")
                    intentos += 1
                
                if intentos > 3:
                    print("Saliendo...")
        
    except KeyboardInterrupt:
        print("Saliendo del programa...")