from abc import ABC, abstractmethod


class Paquete(ABC):

    def __init__(self, id_paquete, nombre, precio_base, proveedor_id):
        self.id_paquete = id_paquete
        self.nombre = nombre
        self.precio_base = precio_base
        self.proveedor_id = proveedor_id

    @property
    def precio_base(self):
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor):

        valor = float(valor)
        if valor <= 0: raise ValueError("El precio base debe ser mayor que cero.")
        self._precio_base = valor

    @abstractmethod
    def calcular_precio_final(self, tipo_cambio=950):
        pass