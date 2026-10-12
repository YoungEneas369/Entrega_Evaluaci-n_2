class Disponibilidad:
    def __init__(self, fecha: str, cupos_disponibles: int):
        self.fecha = fecha
        self.cupos_disponibles = cupos_disponibles

    @property
    def cupos_disponibles(self):
        return self._cupos_disponibles

    @cupos_disponibles.setter
    def cupos_disponibles(self, valor):
        valor = int(valor)
        if valor < 0:
            raise ValueError("Los cupos no pueden ser negativos.")
        self._cupos_disponibles = valor

    def tiene_cupos(self):
        return self.cupos_disponibles > 0

    def descontar_cupo(self):
        if not self.tiene_cupos():
            raise ValueError("No hay cupos disponibles para descontar.")
        self.cupos_disponibles -= 1
