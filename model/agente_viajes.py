from model.trabajador import Trabajador

class AgenteViajes(Trabajador):
    def __init__(self, nombre: str, rut: str):
        super().__init__(nombre, rut)

    def puede_atender_clientes(self):
        return True

    def atender_cliente(self, cliente):
        pass

    def vender_paquete(self, paquete):
        pass
