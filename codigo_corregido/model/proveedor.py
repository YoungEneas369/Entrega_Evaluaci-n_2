from model.disponibilidad import Disponibilidad

class Proveedor:
    def __init__(self, id_proveedor: int, nombre: str):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.disponibilidades = []

    def agregar_disponibilidad(self, disponibilidad: Disponibilidad):
        self.disponibilidades.append(disponibilidad)

    def tiene_cupos(self, fecha: str):
        for disp in self.disponibilidades:
            if disp.fecha == fecha:
                return disp.tiene_cupos()
        return False

    def descontar_cupo(self, fecha: str):
        for disp in self.disponibilidades:
            if disp.fecha == fecha:
                disp.descontar_cupo()
                return True
        raise ValueError("No hay disponibilidad registrada para esta fecha.")