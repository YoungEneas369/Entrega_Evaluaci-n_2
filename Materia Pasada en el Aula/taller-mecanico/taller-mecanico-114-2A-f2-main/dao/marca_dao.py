from dao.dao import DAO
from model.marca import Marca


class MarcaDAO(DAO):
    def crear_tabla(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS marca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL)
        """)

    def insertar(self, marca:Marca): #insertar datos en la tabla
        self.cursor.execute("INSERT INTO marca (nombre) VALUES (?)",(marca.nombre,))
        marca.id = self.cursor.lastrowid

    def buscar(self, id):# Buscar por id de bd un dato
        self.cursor.execute("SELECT id, nombre FROM marca WHERE id = ?",(id,))
        fila= self.cursor.fetchone()
        if fila is None:
            return None
        marca = Marca(fila[1])
        marca.id=fila[0]
        return marca

    def listar(self):#listar todos los registros de la BD
        self.cursor.execute("SELECT id, nombre FROM marca")
        marcas=[]
        for fila in self.cursor.fetchall():
            marca = Marca(fila[1])
            marca.id=fila[0] #Aqui termine de crear el objeto desde el valor de la fila que viene desde el for
            marcas.append(marca)#estoy sumando una marca mas a mis lista de marcas llamada marca
        return marcas

    def actualizar (self, nueva_marca:Marca)->Marca|None:
        self.cursor.execute("UPDATE marca set nombre = ? where id = ?",(nueva_marca.nombre, nueva_marca.id))#actualizo una marca 
        self.conexion.commit()#confirmar y cerrar la transacción
        
        if self.cursor.rowcount==0:
            return None

        return self.buscar(nueva_marca.id)

    def eliminar(self, id:int)->bool:
        self.cursor.execute("DELETE FROM marca where id = ?", (id,))#elimino una marca 
        self.conexion.commit()#confirmar y cerrar la transacción
        return self.cursor.rowcount > 0 #Si o no osea true o false










    


