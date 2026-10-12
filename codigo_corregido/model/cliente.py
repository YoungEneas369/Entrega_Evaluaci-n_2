from model.persona import Persona

class Cliente(Persona):

    def __init__(self, nombre: str, rut: str):
        super().__init__(nombre, rut)
