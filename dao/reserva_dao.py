from dao.dao import DAO

class ReservaDAO(DAO):
    def crear_tabla(self):
        # Tabla principal de Reserva
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS reserva (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_viaje TEXT NOT NULL,
            precio_paquete_clp REAL NOT NULL,
            anticipo REAL NOT NULL,
            estado TEXT NOT NULL
        )
        ''')
        
        # Tabla hija DetalleReserva (Relación 1 a muchos con reserva)
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS detalle_reserva (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reserva_id INTEGER NOT NULL,
            tipo_item TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            FOREIGN KEY(reserva_id) REFERENCES reserva(id)
        )
        ''')
        self.conexion.commit()

    def insertar(self, reserva):
        # 1. Insertamos la transacción principal (Reserva)
        # Usamos parámetros (?) para evitar Inyección SQL
        self.cursor.execute('''
            INSERT INTO reserva (fecha_viaje, precio_paquete_clp, anticipo, estado)
            VALUES (?, ?, ?, ?)
        ''', (reserva.fecha_viaje, reserva.precio_paquete_clp, reserva.anticipo, reserva.estado))
        
        # Obtenemos el ID autogenerado de la reserva recién insertada
        reserva_id = self.cursor.lastrowid
        
        # 2. Insertamos sus líneas de detalle asociadas
        for detalle in reserva.detalles:
            self.cursor.execute('''
                INSERT INTO detalle_reserva (reserva_id, tipo_item, descripcion, cantidad, precio_unitario)
                VALUES (?, ?, ?, ?, ?)
            ''', (reserva_id, detalle.tipo_item.nombre_categoria, detalle.descripcion, detalle.cantidad, detalle.precio_unitario))
        
        # Hacemos commit para guardar toda la transacción junta
        self.conexion.commit()
        return reserva_id

    def buscar_detalles(self, id_reserva):
        self.cursor.execute("SELECT * FROM reserva WHERE id = ?", (id_reserva,))
        res = self.cursor.fetchone()
        if not res:
            return None
            
        self.cursor.execute("SELECT tipo_item, descripcion, cantidad, precio_unitario FROM detalle_reserva WHERE reserva_id = ?", (id_reserva,))
        detalles = self.cursor.fetchall()
        return {"reserva": res, "detalles": detalles}

