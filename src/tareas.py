from utils import Database, CONFIG

class Tareas:
    def __init__(self, db: Database, usuario_id):
        self.db = db
        self.usuario_id = usuario_id

    def agregar_tarea(self, tarea, hora=None, prioridad=1):
        sql = """ INSERT INTO tareas (usuario_id, hora, tarea, prioridad)
        VALUES (%s, %s, %s, %s)
        """
        params = (self.usuario_id, hora, tarea, prioridad)
        self.db.conectar()
        self.db.ejecutar(sql, (params), commit=True)
        print("Tarea agregada con exito")

        self.db.cerrar()
    def ver_tareas(self):
        self.db.conectar() 
        sql = "SELECT id, hora, tarea, prioridad FROM tareas WHERE usuario_id = %s"
        cursor = self.db.ejecutar(sql, (self.usuario_id,))
        tareas = cursor.fetchall()
        for t in tareas:
            print("Tus tareas")
            print(f"[{t[0]}] {t[1]} | {t[2]} | Prioridad: {t[3]}")
        if not tareas:
            print("No tienes tareas registradas\n")

        self.db.cerrar()

    
    def eliminar_tareas(self, tarea_id):
        self.db.conectar()
        sql = "DELETE FROM tareas WHERE id = %s AND usuario_id = %s"
        params = (tarea_id, self.usuario_id)
        self.db.ejecutar(sql, params, commit=True)
        print("\n🗑️ Tarea eliminada")

    
    