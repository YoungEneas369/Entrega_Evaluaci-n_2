from dao.dao import DAO
from model.paquete_nacional import PaqueteNacional
from model.paquete_internacional import PaqueteInternacional
from model.paquete_crucero import PaqueteCrucero

class PaqueteDAO(DAO):
    def crear_tabla(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS paquete (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio_base REAL NOT NULL,
        tipo TEXT NOT NULL)
        ''')

    def insertar(self, paquete, tipo):
        self.cursor.execute("INSERT INTO paquete (nombre, precio_base, tipo) VALUES (?, ?, ?)", 
                            (paquete.nombre, paquete.precio_base, tipo))
        self.conexion.commit()
        paquete.id_paquete = self.cursor.lastrowid

    def buscar(self, id):
        self.cursor.execute("SELECT id, nombre, precio_base, tipo FROM paquete WHERE id = ?", (id,))
        fila = self.cursor.fetchone()
        if fila is None:
            return None
        
        tipo = fila[3]
        if tipo == 'nacional':
            p = PaqueteNacional(fila[0], fila[1], fila[2], None)
        elif tipo == 'internacional':
            p = PaqueteInternacional(fila[0], fila[1], fila[2], None)
        else:
            p = PaqueteCrucero(fila[0], fila[1], fila[2], None)
            
        return p

    def listar(self):
        self.cursor.execute("SELECT id, nombre, precio_base, tipo FROM paquete")
        paquetes = []
        for fila in self.cursor.fetchall():
            tipo = fila[3]
            if tipo == 'nacional':
                p = PaqueteNacional(fila[0], fila[1], fila[2], None)
            elif tipo == 'internacional':
                p = PaqueteInternacional(fila[0], fila[1], fila[2], None)
            else:
                p = PaqueteCrucero(fila[0], fila[1], fila[2], None)
            paquetes.append((p, tipo))
        return paquetes

    def actualizar(self, paquete, tipo):
        self.cursor.execute("UPDATE paquete SET nombre = ?, precio_base = ?, tipo = ? WHERE id = ?", 
                            (paquete.nombre, paquete.precio_base, tipo, paquete.id_paquete))
        self.conexion.commit()

    def eliminar(self, id):
        self.cursor.execute("DELETE FROM paquete WHERE id = ?", (id,))
        self.conexion.commit()
        return self.cursor.rowcount > 0
