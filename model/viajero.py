from model.persona import Persona

class Viajero(Persona):
    def __init__(self, rut, nombre, numero_pasaporte):
        super().__init__(nombre, rut)
        self.numero_pasaporte = numero_pasaporte

    @property
    def numero_pasaporte(self):
        return self.__numero_pasaporte

    @numero_pasaporte.setter
    def numero_pasaporte(self, valor):
        if not valor or str(valor).strip() == "":
            raise ValueError("El pasaporte no puede estar vacío.")
        
        valor = str(valor).strip().upper()
        if not valor.isalnum() or len(valor) < 6 or len(valor) > 12:
            raise ValueError("Pasaporte inválido. Debe tener entre 6 y 12 caracteres.")
            
        self.__numero_pasaporte = valor
