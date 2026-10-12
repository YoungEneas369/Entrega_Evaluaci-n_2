from model.persona import Persona
from abc import ABC

class Trabajador(Persona, ABC):
    def __init__(self, nombre: str, rut: str):
        super().__init__(nombre, rut)
