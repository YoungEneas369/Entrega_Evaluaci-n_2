from model.trabajador import Trabajador

class Administrador(Trabajador):
    def __init__(self, nombre: str, rut: str):
        super().__init__(nombre, rut)

    def puede_atender_clientes(self):
        return False

    def gestionar_proveedor(self, proveedor):
        pass

    def gestionar_pagos(self, reserva):
        pass
